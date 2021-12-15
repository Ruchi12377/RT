"""
 @file select.py
 @brief hannisiteisuruprogram
 @date $Date$


"""

import RTC
import OpenRTM_aist
import Img
import sys
import time
import tkinter
from datetime import datetime
from PIL import Image, ImageTk
import os 
import numpy
import cv2
sys.path.append(".")

select_spec = ["implementation_id", "select",
		 "type_name",         "select",
		 "description",       "hannisiteisuruprogram",
		 "version",           "1.0.0",
		 "vendor",            "Hayashi",
		 "category",          "main",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.hanni", "select",

		 "conf.__widget__.hanni", "radio",
		 "conf.__constraints__.hanni", "(select,up_right,down_right,up_left,down_left,all)",

         "conf.__type__.hanni", "string",

		 ""]

class select(OpenRTM_aist.DataFlowComponentBase):

	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Img = OpenRTM_aist.instantiateDataType(Img.TimedCameraImage)
		"""
		"""
		self._ImgIn = OpenRTM_aist.InPort("Img", self._d_Img)
		self._d_Trans = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._TransOut = OpenRTM_aist.OutPort("Trans", self._d_Trans)

		"""
		
		 - Name:  config
		 - DefaultValue: select
		"""
		self._config = ['select']


	def onInitialize(self):
		self.bindParameter("hanni", self._config, "select")

		self.addInPort("Img",self._ImgIn)

		self.addOutPort("Trans",self._TransOut)

		return RTC.RTC_OK
	
	def create_canvas(self):

		# ドラッグ開始
		def start_point_get(event):

			global start_x, start_y 

			canvas1.delete("rect1")  # rect1を検査

			# canvasに四角形を描画
			canvas1.create_rectangle(event.x, event.y, event.x + 1, event.y + 1, outline="red", tag="rect1")
			
			start_x, start_y = event.x, event.y

		# ドラッグ中
		def rect_drawing(event):

			# 領域外に出た時の処理
			if event.x < 0:
				end_x = 0
			else:
				end_x = min(img.width, event.x)
			if event.y < 0:
				end_y = 0
			else:
				end_y = min(img.height, event.y)

			# 再描画
			canvas1.coords("rect1", start_x, start_y, end_x, end_y)

		# ドラッグを離したとき
		def release_action(event):

			# 再取得
			start_x, start_y, end_x, end_y = [
				round(n) for n in canvas1.coords("rect1")
			]
			
			self._d_Trans.data = (str(start_x) + "," + str(start_y) + "," + str(end_x) + "," + str(end_y))
			self._TransOut.write()
			
			root.destroy()
			self.state = False

		
		if self.state == True:

			img_open = Image.fromarray(self.img_in[:, :, ::-1].copy())
			img = img_open.resize((1000, 300))

			root = tkinter.Tk()
			# tkinter用に画像変換
			img_tk = ImageTk.PhotoImage(img)

			# Canvas描画
			canvas1 = tkinter.Canvas(root, width=img.width, height=img.height)
			# 取得した画像表示
			canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

			# マウス処理
			canvas1.pack()
			canvas1.bind("<ButtonPress-1>", start_point_get)
			canvas1.bind("<Button1-Motion>", rect_drawing)
			canvas1.bind("<ButtonRelease-1>", release_action)

			root.mainloop()

	def onActivated(self, ec_id):

		self.path = str(os.path.dirname(__file__) + "\\img\\photo.jpg")
		self.state = False
	
		return RTC.RTC_OK

	#def onDeactivated(self, ec_id):
	#
	# 	return RTC.RTC_OK

	def onExecute(self, ec_id):

		if not self._ImgIn.isNew():
			return RTC.RTC_OK

		data = self._ImgIn.read()
		self.img_in = numpy.frombuffer(data.data.image.raw_data, numpy.uint8).reshape((data.data.image.height, data.data.image.width, 3))
		self.img_in = cv2.cvtColor(self.img_in, cv2.COLOR_BGRA2BGR)
		self.state = True
		self.create_canvas()
	
		return RTC.RTC_OK


def selectInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=select_spec)
    manager.registerFactory(profile,
                            select,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    selectInit(manager)

    # Create a component
    comp = manager.createComponent("select")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

