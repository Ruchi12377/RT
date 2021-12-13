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
import serial

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
		 "conf.default.port", "'/dev/ttyACM0'",

		 "conf.__widget__.W_width", "text",
		 "conf.__widget__.W_height", "text",
		 "conf.__widget__.M_power_width", "text",
		 "conf.__widget__.M_power_height", "text",
		 "conf.__widget__.port", "text",

         "conf.__type__.W_width", "int",
         "conf.__type__.W_height", "int",
         "conf.__type__.M_power_width", "int",
         "conf.__type__.M_power_height", "int",
         "conf.__type__.port", "string",

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
		"""
		
		 - Name:  port
		 - DefaultValue: /dev/ttyACM0
		"""
		self._port = ['/dev/ttyACM0']

	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("W_width", self._W_width, "1000")
		self.bindParameter("W_height", self._W_height, "300")
		self.bindParameter("M_power_width", self._M_power_width, "10")
		self.bindParameter("M_power_height", self._M_power_height, "10")
		self.bindParameter("port", self._port, "'/dev/ttyACM0'")

		# Set InPort buffers
		self.addInPort("Trans",self._TransIn)

		# Set OutPort buffers
		self.addOutPort("State",self._StateOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	def onActivated(self, ec_id):

		#消す部分の始点、終点の座標変数を定義(cm)
		self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0

		ser = serial.Serial(str(self.port), 9600)

		return RTC.RTC_OK

	def move_main(self):

		direy = 0.5

		self.act_height = round(self._M_power_height * self.end_y / self._W_height)
		self.act_width = round(self._M_power_width * self.end_x / self._W_width)
		
		ser.write(b"rot " + str(act_height))
		time.sleep(direy)
		ser.write(b"rot " + str(-act_height))

		self.init()
	
	def init(self):

		ser.close()

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

