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

		#シリアル通信の準備を行う
		ser = serial.Serial(port, 9600)
		#シリアル通信が終わるまで待つ
		time.sleep(3)

		#シリアルでデータを送るための関数
		def send(data):
			ser.write(bytes(data, "utf-8"))

		#arduino側の機能を呼び出すための関数群
		def init(x, y, z):
			send("init {0} {1} {2}".format(x, y, z))
		def reset():
			ser.write(b"reset")
		def moveX(rate):
			send("moveX {0}".format(rate))
		def moveY(rate):
			send("moveY {0}".format(rate))
		def moveZ(rate):
			send("moveZ {0}".format(rate))
		def rot(direction, value):
			send("rot {0} {1}".format(direction, value))

		#100移動に対して15秒かかるので
		def getMoveXTime(amount):
			return math.ceil(15.0 / 100.0 * amount)
		def getMoveYTime(amount):
			return math.ceil(15.0 / 75.0 * amount)

		#boardの大きさを初期化
		init(self._board_hard_width, self._board_hard_height, self._board_hard_depth)
		time.sleep(3)

		def pixelToRate(rtPixel, rtSize, hardSize):
			return math.ceil(rtPixel / rtSize * hardSize)

		def eraser(start_x_rate, start_y_rate, end_x_rate, end_y_rate, ):
			start_x = math.ceil(start_x_rate * self._board_hard_width / 100)
			start_y = math.ceil(start_y_rate * self._board_hard_height / 100)
			end_x = math.ceil(end_x_rate * self._board_hard_width / 100)
			end_y = math.ceil(end_y_rate * self._board_hard_height / 100)

			moveX(start_x_rate)
			time.sleep(getMoveXTime(start_x_rate))
			print(start_x_rate)

			moveY(start_y_rate)
			time.sleep(getMoveYTime(start_y_rate))
			print(start_y_rate)

			#何回ループするか
			l = math.ceil((end_x - start_x) / self._core_hard_width) + 2
			for i in range(1, l):
				targetX = start_x + self._core_hard_width * i
				targetXRate = math.ceil(targetX / self._board_hard_width * 100)
				
				if(i % 2 == 1):
					targetYRate = end_y_rate
				else:
					targetYRate = start_y_rate
				
				#押し込み処理を入れる
				#moveZ(any value...)
				
				#上か下まで移動させる
				moveY(targetYRate)

				time.sleep(getMoveYTime(targetYRate))

				#最後だけYを移動する
				if(i == l - 1):
					break

				#横移動
				moveX(targetXRate)
				print(targetXRate)
				time.sleep(getMoveXTime(targetXRate))

			print("reset")
			reset()

		eraser(10, 20, 40, 50)
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
			self.getMove()

		return RTC.RTC_OK

	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK



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

