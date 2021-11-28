#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file move.py
 @brief hannisiteisuruprogram
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import RPi.GPIO as GPIO
import serial

PUL = 17
DIR = 27
ENA = 22 

move_spec = ["implementation_id", "move",
		 "type_name",         "move",
		 "description",       "hannisiteisuruprogram",
		 "version",           "1.0.0",
		 "vendor",            "Hayashi",
		 "category",          "main",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 "conf.default.W_width", "1000",
		 "conf.default.W_height", "300",
		 "conf.default.M_power_width", "10",
		 "conf.default.M_power_height", "10",

		 "conf.__widget__.W_width", "slider",
		 "conf.__widget__.W_height", "slider",
		 "conf.__widget__.M_power_width", "slider",
		 "conf.__widget__.M_power_height", "slider",
		 "conf.__constraints__.W_width", "0<, 2000>",
		 "conf.__constraints__.W_height", "0<, 500>",
		 "conf.__constraints__.M_power_width", "0<, 100>",
		 "conf.__constraints__.M_power_height", "0<, 100>",

         "conf.__type__.W_width", "int",
         "conf.__type__.W_height", "int",
         "conf.__type__.M_power_width", "int",
         "conf.__type__.M_power_height", "int",

		 ""]

class move(OpenRTM_aist.DataFlowComponentBase):

	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_Trans = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._TransIn = OpenRTM_aist.InPort("Trans", self._d_Trans)
		self._d_State = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StateOut = OpenRTM_aist.OutPort("State", self._d_State)

		"""
		
		 - Name:  W_width
		 - DefaultValue: 1000
		"""
		self._W_width = [1000]
		"""
		
		 - Name:  W_height
		 - DefaultValue: 300
		"""
		self._W_height = [300]
		"""
		
		 - Name:  M_power_width
		 - DefaultValue: 10
		"""
		self._M_power_width = [10]
		"""
		
		 - Name:  M_power_height
		 - DefaultValue: 10
		"""
		self._M_power_height = [10]

	def onInitialize(self):

		self.bindParameter("W_width", self._W_width, "1000")
		self.bindParameter("W_height", self._W_height, "300")
		self.bindParameter("M_power_width", self._M_power_width, "10")
		self.bindParameter("M_power_height", self._M_power_height, "10")

		self.addInPort("Trans",self._TransIn)

		self.addOutPort("State",self._StateOut)


		return RTC.RTC_OK

	def onActivated(self, ec_id):

		#消す部分の始点、終点の座標変数を定義(cm)
		self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0

		ser = serial.Serial("Hard", 9600)

		ser.write(b"init 1000 300 10")

		return RTC.RTC_OK

	def move_main(self):

		#横方向に始点まで回転させなければならないかを定義
		need_rotate_x_F = self.start_x / self._M_power_width
		#横方向に終点まで回転させなければならないかを定義
		need_rotate_x_E = self.end_x / self._M_power_width
		#縦方向に何回転させなければならないかを定義
		need_rotate_y = self.end_y / self._M_power_height
		#操作にディレイを掛けるための変数を定義
		direy = 0.5
		#コア部分の横の長さはモータ何回転分か
		core_width = 5

		#シリアル通信を用いてX方向に制御
		ser.write(b"moveX" + str(need_rotate_x_F))
		#おしつけ
		ser.write(b"moveZ true")
		#ループ終了判定用の変数
		flag = 0

		while flag <= self.end_x:
			#シリアル通信を用いてY方向に制御
			ser.write(b"moveY" + str(need_rotate_y))
			ser.write(b"moveX" + str(core_width))
			flag += core_width
			time.sleep(direy)
			ser.write(b"moveY" + str(-need_rotate_y))
			ser.write(b"moveX" + str(core_width))
			flag += core_width
			time.sleep(direy)
		
		ser.write(b"moveZ false")
		self._d_State = True
		self._StateOut.write()

	def onExecute(self, ec_id):

		if self._TransIn.isNew():
			self._d_Trans = self._TransIn.read()
			num = self._d_Trans.data
			start_x_num = num.find(",")
			self.start_x = int(num[0:start_x_num])
			start_y_num = num.find(",", start_x_num + 1)
			self.start_y = int(num[start_x_num + 1:start_y_num])
			end_x_num = num.find(",", start_y_num + 1)
			self.end_x = int(num[start_y_num + 1:end_x_num])
			end_y_num = num.find(",", end_x_num + 1)
			self.end_y = int(num[end_x_num + 1:len(num)])
			self.move_main()
	
		return RTC.RTC_OK

def moveInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=move_spec)
    manager.registerFactory(profile,
                            move,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    moveInit(manager)

    # Create a component
    comp = manager.createComponent("move")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

