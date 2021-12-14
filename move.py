"""
 @file move.py
 @brief hannisiteisuruprogram
 @date $Date$


"""

import RTC
import sys
import time
import math
import serial
import OpenRTM_aist
import morter as m
sys.path.append(".")

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
		 "conf.default.M_power_width", "100",
		 "conf.default.M_power_height", "75",
		 "conf.default.port", "COM4",
		 "conf.default.M_power_push", "20",
		 "conf.default.core_hard_width", "9",

		 "conf.__widget__.W_width", "text",
		 "conf.__widget__.W_height", "text",
		 "conf.__widget__.M_power_width", "text",
		 "conf.__widget__.M_power_height", "text",
		 "conf.__widget__.port", "text",
		 "conf.__widget__.M_power_push", "text",
		 "conf.__widget__.core_hard_width", "text",

         "conf.__type__.W_width", "int",
         "conf.__type__.W_height", "int",
         "conf.__type__.M_power_width", "int",
         "conf.__type__.M_power_height", "int",
         "conf.__type__.port", "string",
         "conf.__type__.M_power_push", "int",
         "conf.__type__.core_hard_width", "int",

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
		
		 - Name:  board_rt_width
		 - DefaultValue: 1000
		"""
		self._board_rt_width = [1000]
		"""
		
		 - Name:  board_rt_height
		 - DefaultValue: 300
		"""
		self._board_rt_height = [300]
		"""
		
		 - Name:  board_hard_width
		 - DefaultValue: 100
		"""
		self._board_hard_width = [100]
		"""
		
		 - Name:  board_hard_height
		 - DefaultValue: 75
		"""
		self._board_hard_height = [75]
		"""
		
		 - Name:  port
		 - DefaultValue: COM4
		"""
		self._port = ['COM4']
		"""
		
		 - Name:  board_hard_depth
		 - DefaultValue: 20
		"""
		self._board_hard_depth = [20]
		"""
		
		 - Name:  core_hard_width
		 - DefaultValue: 9
		"""
		self._core_hard_width = [9]


	def onInitialize(self):

		self.bindParameter("W_width", self._board_rt_width, "1000")
		self.bindParameter("W_height", self._board_rt_height, "300")
		self.bindParameter("M_power_width", self._board_hard_width, "100")
		self.bindParameter("M_power_height", self._board_hard_height, "75")
		self.bindParameter("port", self._port, "COM4")
		self.bindParameter("M_power_push", self._board_hard_depth, "20")
		self.bindParameter("core_hard_width", self._core_hard_width, "9")

		self.addInPort("Trans",self._TransIn)

		self.addOutPort("State",self._StateOut)

		return RTC.RTC_OK

	def onActivated(self, ec_id):
		
		self.start_x = 0
		self.start_y = 0
		self.end_x = 0
		self.end_y = 0
		self.start_x_rate = 0
		self.start_y_rate = 0
		self.end_x_rate = 0
		self.end_y_rate = 0

		return RTC.RTC_OK

	def getMove(self):

		m.initialize(self._port, self._board_hard_width, self._board_hard_height, self._board_hard_depth, self._core_hard_width, self._board_rt_width, self._board_rt_height)
		self.start_x_rate = m.pixelToRate(self.start_x, self._board_rt_width, self._board_hard_width)
		self.start_y_rate = m.pixelToRate(self.start_y, self._board_rt_height, self._board_hard_height)
		self.end_x_rate = m.pixelToRate(self.end_x, self._board_rt_width, self._boboard_hard_width)
		self.end_y_rate = m.pixelToRate(self.end_y, self._board_rt_height, self._board_hard_height)

		m.eraser(self.start_x_rate, self.start_y_rate, self.end_x_rate, self.end_y_rate)


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
			self.getMove()

		return RTC.RTC_OK

	def onDeactivated(self, ec_id):

		m.dispose()
	
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

