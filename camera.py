"""
 @file camera.py
 @brief hannisiteisuruprogram
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC

import OpenRTM_aist
import cv2
import time
import os

camera_spec = ["implementation_id", "camera",
		 "type_name",         "camera",
		 "description",       "hannisiteisuruprogram",
		 "version",           "1.0.0",
		 "vendor",            "Hayashi",
		 "category",          "main",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]

class camera(OpenRTM_aist.DataFlowComponentBase):

	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_State = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._StateIn = OpenRTM_aist.InPort("State", self._d_State)
		self._d_Trans = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._TransIn = OpenRTM_aist.InPort("Trans", self._d_Trans)
		self._d_Path = OpenRTM_aist.instantiateDataType(RTC.TimedString)
		"""
		"""
		self._PathOut = OpenRTM_aist.OutPort("Path", self._d_Path)
		self._d_Back = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
		"""
		"""
		self._BackOut = OpenRTM_aist.OutPort("Back", self._d_Back)
		
	def onInitialize(self):
		# Bind variables and configuration variable

		# Set InPort buffers
		self.addInPort("State",self._StateIn)
		self.addInPort("Trans",self._TransIn)

		# Set OutPort buffers
		self.addOutPort("Path",self._PathOut)
		self.addOutPort("Back",self._BackOut)

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	def onActivated(self, ec_id):
		self.state = False
		self.start_x, self.start_y, self.end_x, self.end_y = 100, 200, 300, 400
		#パスを指定
		self.path = str(os.path.dirname(__file__) + "\\img\\photo.jpg")

		return RTC.RTC_OK
	
	def Capture(self):

		print("撮影したいタイミングでyを、中断したい場合はnを押してください")
		#カメラ番号指定
		cap = cv2.VideoCapture(1)
		while True:
			#リアルタイムでカメラ映像をウィンドウ上に表示する
			ret, frame = cap.read()
			cv2.imshow("camera", frame)

			#キーボード入力町
			k = cv2.waitKey(1)&0xff
			#特定のキーボード入力を待つ。ここでは[Y]と[N]
			if k == ord('y'):
				
				#写真を撮影してあらかじめ指定したファイルに保存
				cv2.imwrite(self.path, frame)
				#受け取った座標でトリミング
				dst_img = cv2.imread(self.path)
				dst = dst_img[self.start_y:self.end_y,self.start_x:self.end_x, :]
				#トリミングした写真を保存
				cv2.imwrite(self.path, dst)

				#写真のパスを渡す
				self._d_Path.data = self.path
				self._PathOut.write()
				#処理を繰り返さないようFalseに
				self.state = False
				self._d_State.data = False
				#カメラのハンドル開放とウィンドウの削除
				cap.release()
				cv2.destroyAllWindows()
				#ループ処理終了
				break

			#途中終了用処理
			elif k == ord('n'):
				i = 4
				while i > 1:
					i -= 1
					print(str(i) + "秒後に終了します")
					time.sleep(1)
				#startへ信号を送る
				self._d_Back.data = True
				self._BackOut.write()
				self.state = False
				self._d_State.data = False
				cap.release()
				cv2.destroyAllWindows()
				break


	def onExecute(self, ec_id):
		
		#Startからの信号受け取り
		if self._StateIn.isNew():
			self._d_State = self._StateIn.read()
			self.state = self._d_State.data
		
		#受け取った座標のデータを分解してint型に変換
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
		
		#指示を受け取った際に関数実行
		if self.state == True:
			self.Capture()
	
		return RTC.RTC_OK




def cameraInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=camera_spec)
    manager.registerFactory(profile,
                            camera,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    cameraInit(manager)

    # Create a component
    comp = manager.createComponent("camera")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

