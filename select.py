#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file select.py
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
from PIL import Image, ImageTk
from datetime import datetime
import os


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
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
		 "conf.default.template", "range_specification",

		 "conf.__widget__.template", "radio",
		 "conf.__constraints__.template", "(range_specification,up_right,down_right,up_left,down_left)",

         "conf.__type__.template", "string",

		 ""]

class select(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Path = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._PathIn = OpenRTM_aist.InPort("Path", self._d_Path)
		self._d_Trans = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._TransOut = OpenRTM_aist.OutPort("Trans", self._d_Trans)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  config
		 - DefaultValue: range_specification
		"""
		self._config = ['range_specification']

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("template", self._config, "range_specification")

		# Set InPort buffers
		self.addInPort("Path",self._PathIn)

		# Set OutPort buffers
		self.addOutPort("Trans",self._TransOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

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

			img_open = Image.open(self.path)
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

		self.path = "ここにファイルのパスを格納する"
		self.state = False

		return RTC.RTC_OK

	def onExecute(self, ec_id):

		if self._PathIn.isNew():
			self._d_Path = self._PathIn.read()
			self.path = self._d_Path.data
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

