import serial 
import time
import math

#port = "/dev/cu.usbmodem21101"
port = "COM4"

#ハードウェア側の大きさ
board_hard_width = 100
board_hard_height = 75
board_hard_depth = 2
core_hard_width = 9

#RTが扱うハードの大きさ
board_rt_width = 1000
board_rt_height = 300

#仮
# start_x = 100
# start_y = 100
# end_x = 50
# end_y = 200

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

def sizeToRate(target, width):
    return 

#100移動に対して15秒かかるので
def getMoveXTime(amount):
    return math.ceil(15.0 / 100.0 * amount / 2.0)
def getMoveYTime(amount):
    return math.ceil(15.0 / 75.0 * amount / 2.0)

#boardの大きさを初期化
init(board_hard_width, board_hard_height, board_hard_depth)
time.sleep(3)

def eraser(start_x_rate, start_y_rate, end_x_rate, end_y_rate, ):
    start_x = math.ceil(start_x_rate * board_hard_width / 100)
    start_y = math.ceil(start_y_rate * board_hard_width / 100)
    end_x = math.ceil(end_x_rate * board_hard_height / 100)
    end_y = math.ceil(end_y_rate * board_hard_height / 100)

    xRate = start_x_rate
    yRate = start_y_rate
    moveX(xRate)
    time.sleep(getMoveXTime(xRate))
    moveY(yRate)
    time.sleep(getMoveYTime(yRate))

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
        #moveZ(100)
        
        #上か下まで移動させる
        moveY(targetYRate)

        time.sleep(getMoveYTime(targetYRate))

        #最後だけYを移動する
        if(i == l - 1): 
            #引く処理を入れる
            #moveZ(0)
            break

        #横移動
        moveX(targetXRate)
        time.sleep(getMoveXTime(targetXRate))

    #moveZ(push)
    print("reset")
    reset()

eraser(10, 20, 40, 50)
ser.close()