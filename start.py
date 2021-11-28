#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file start.py
 @brief hannisiteisuruprogram
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import tkinter
import time
import pyautogui
from PIL import Image, ImageTk
import cv2
from datetime import datetime
import os


start_spec = ["implementation_id", "start",
		 "type_name",         "start",
		 "description",       "hannisiteisuruprogram",
		 "version",           "1.0.0",
		 "vendor",            "Hayashi",
		 "category",          "main",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]

class start(OpenRTM_aist.DataFlowComponentBase):

	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Start = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StartIn = OpenRTM_aist.InPort("Start", self._d_Start)
		self._d_Back = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._BackIn = OpenRTM_aist.InPort("Back", self._d_Back)
		self._d_State = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StateOut = OpenRTM_aist.OutPort("State", self._d_State)
		self._d_Trans = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._TransOut = OpenRTM_aist.OutPort("Trans", self._d_Trans)

	def onInitialize(self):

		self.addInPort("Start",self._StartIn)
		self.addInPort("Back",self._BackIn)

		# Set OutPort buffers
		self.addOutPort("State",self._StateOut)
		self.addOutPort("Trans",self._TransOut)

		return RTC.RTC_OK


	def onActivated(self, ec_id):

		#写真を保存するためのファイルを作成する
		p = str(os.path.dirname(__file__)) + "\\img"
		if os.path.exists(p) == False:
			os.mkdir(p)
			
		self.back = False
		self.settings()

		return RTC.RTC_OK

	def settings(self):

		cap = cv2.VideoCapture(1)
		path = str(os.path.dirname(__file__) + "\\img\\photo.jpg")
		dst_img_path = str(os.path.dirname(__file__) + "\\img\\photo_dst.jpg")

		def start_point_get(event):
			global start_x, start_y 
			canvas1.delete("rect1")
			canvas1.create_rectangle(event.x, event.y, event.x + 1, event.y + 1,outline="red", tag="rect1")
			start_x, start_y = event.x, event.y

		def rect_drawing(event):

			if event.x < 0:
				end_x = 0
			else:
				end_x = min(img.width, event.x)
			if event.y < 0:
				end_y = 0
			else:
				end_y = min(img.height, event.y)

			canvas1.coords("rect1", start_x, start_y, end_x, end_y)

		def release_action(event):

			start_x, start_y, end_x, end_y = [
				round(n) for n in canvas1.coords("rect1")
			]

			dst_img = cv2.imread(path)
			dst = dst_img[start_y:end_y,start_x:end_x, :]
			cv2.imshow("dst_img", dst)

			print("これでよろしいですか？")
			self.root.destroy()
			while True:
				wait1 = input(">>")
				if wait1 == "y":
					self._d_Trans.data = (str(start_x) + "," + str(start_y) + "," + str(end_x) + "," + str(end_y))
					self._TransOut.write()
					self._d_State.data = True
					self._StateOut.write()
					self._d_Back.data = False
					self.back = False
					
					cap.release()
					cv2.destroyAllWindows()
					break
				elif wait1 == "n":
					print("もう一度選択してください")
					break

		print("初回起動やカメラの位置を動かした場合には[y]を入力してください。それ以外の場合は[n]を入力してください")
		while True:
			wait = input(">>")

			if wait == "y":
				print("ホワイトボードの位置をドラッグ操作で選択してください")
				self.root = tkinter.Tk()
				ret, frame = cap.read()
				cv2.imwrite(path, frame)
				img = Image.open(path)

				img_tk = ImageTk.PhotoImage(img)

				canvas1 = tkinter.Canvas(self.root, bg="white", width=int(img.width), height=int(img.height))
				canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

				canvas1.pack()
				canvas1.bind("<ButtonPress-1>", start_point_get)
				canvas1.bind("<Button1-Motion>", rect_drawing)
				canvas1.bind("<ButtonRelease-1>", release_action)

				self.root.mainloop()

				print("終了できている")
				break

			elif wait == "n":
				self._d_State.data = True
				self._StateOut.write()
				#変数初期化
				self._d_Back.data = False
				self.back = False
				break

	def onExecute(self, ec_id):

		#カメラからの処理を受け取った時の処理
		if self._BackIn.isNew():
			self._d_Back = self._BackIn.read()
			self.back = self._d_Back.data
			self._d_State.data = False
		
		if self.back == True:
			self.settings()
	
		return RTC.RTC_OK




def startInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=start_spec)
    manager.registerFactory(profile,
                            start,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    startInit(manager)

    # Create a component
    comp = manager.createComponent("start")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

