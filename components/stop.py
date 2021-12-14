"""
 @file stop.py
 @brief hannisiteisuruprogram
 @date $Date$


"""
import sys
import time
sys.path.append(".")

import RTC
import OpenRTM_aist

stop_spec = ["implementation_id", "stop",
		 "type_name",         "stop",
		 "description",       "hannisiteisuruprogram",
		 "version",           "1.0.0",
		 "vendor",            "Hayashi",
		 "category",          "main",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]
		 
class stop(OpenRTM_aist.DataFlowComponentBase):

	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_State = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StateIn = OpenRTM_aist.InPort("State", self._d_State)
		self._d_Start = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StartOut = OpenRTM_aist.OutPort("Start", self._d_Start)

	def onInitialize(self):

		self.addInPort("State",self._StateIn)

		self.addOutPort("Start",self._StartOut)

		return RTC.RTC_OK

	def onActivated(self, ec_id):

		self.state = False
	
		return RTC.RTC_OK

	def onExecute(self, ec_id):

		if self._StateIn.isNew():
			self._d_State = self._StateIn.read()
			self.state = self._d_State.data
	
		return RTC.RTC_OK


def stopInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=stop_spec)
    manager.registerFactory(profile,
                            stop,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    stopInit(manager)

    # Create a component
    comp = manager.createComponent("stop")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

