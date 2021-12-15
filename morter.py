import serial 
import time
import math

#port = "/dev/cu.usbmodem21101"
#port = "COM4"

#ハードウェア側の大きさ
board_hard_width =0 
board_hard_height = 0
board_hard_depth = 0
core_hard_width = 0

#RTが扱うハードの大きさ
board_rt_width = 0
board_rt_height = 0

is_init_module = False
is_init_hard = False

#シリアル通信の準備を行う
ser = serial.Serial()

def initialize(port, width, height, depth, core_width, rt_width, rt_height):

    global is_init_module
    global ser

    global board_hard_width
    global board_hard_height
    global board_hard_depth
    global core_hard_width
    global board_rt_width
    global board_rt_height

    #初期化が住んでいるので
    if(is_init_module == True):
        return

    board_hard_width = width
    board_hard_height = height
    board_hard_depth = depth
    core_hard_width = core_width
    board_rt_width = rt_width
    board_rt_height = rt_height
    #シリアル通信が終わるまで待つ
    ser = serial.Serial(port, 9600)
    if(ser.is_open == False):
        ser.open()
    ser.reset_input_buffer()
    time.sleep(3)
    is_init_module = True
    
def dispose():

    global is_init_module
    global ser

    #初期化が住んでいないので
    if(is_init_module == False):
        return
    time.sleep(10)
    ser.close()
    is_init_hard = False
    is_init_module = False

#シリアルでデータを送るための関数
def send(data):
    global ser
    global is_init_module
    print("send")
    #初期化が住んでいないので
    if(is_init_module == False):
        print("return")
        return
    print("write")

    ser.write(bytes(data, "utf-8"))

#arduino側の機能を呼び出すための関数群
def init(x, y, z):
    print("init")
    global is_init_hard
    is_init_hard = True
    print("init2")
    send("init {0} {1} {2}".format(x, y, z))
    print("sleep")
    time.sleep(2)
    print("init3")
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
#init(board_hard_width, board_hard_height, board_hard_depth)

def pixelToRate(rtPixel, rtSize, hardSize):
    return math.ceil(rtPixel / rtSize * hardSize)

def eraser(start_x_rate, start_y_rate, end_x_rate, end_y_rate, ):
    global board_hard_width
    global board_hard_height
    global core_hard_width

    start_x = math.ceil(start_x_rate * board_hard_width / 100)
    start_y = math.ceil(start_y_rate * board_hard_height / 100)
    end_x = math.ceil(end_x_rate * board_hard_width / 100)
    end_y = math.ceil(end_y_rate * board_hard_height / 100)

    moveX(start_x_rate)
    time.sleep(getMoveXTime(start_x_rate))
    print(start_x_rate)

    moveY(start_y_rate)
    time.sleep(getMoveYTime(start_y_rate))
    print(start_y_rate)

    #何回ループするか
    l = math.ceil((end_x - start_x) / core_hard_width) + 2
    for i in range(1, l):
        targetX = start_x + core_hard_width * i
        targetXRate = math.ceil(targetX / board_hard_width * 100)
        
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
            #moveZ(0)
            break

        #横移動
        moveX(targetXRate)
        print(targetXRate)
        time.sleep(getMoveXTime(targetXRate))

    print("reset")
    reset()
