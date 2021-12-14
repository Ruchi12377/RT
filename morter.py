import serial 
import time

port = "COM4"
direy = 3

power_width = 100
power_height = 75
power_push = 2
W_width = 1000
W_height = 300
start_x, start_y, end_x, end_y = 100, 100, 500, 200
flag = 0
flag1 = 1
core_width = 9

act_height_s = round(100 * start_y / W_height)
act_width_s = round(100 * start_x / W_width)
act_height_f = round(100 * end_y / W_height)
act_width_f = round(100 * end_x / W_width)

print(act_width_s,act_width_f,act_height_s,act_height_f)

ser = serial.Serial("COM4", 9600, timeout= 60)
time.sleep(3)

def init(x, y, z):
    ser.write(bytes("init {0} {1} {2}".format(x, y, z), "utf-8"))
def reset():
    ser.write(b"reset")
def moveX(rate):
    ser.write(bytes("moveX {0}".format(rate), "utf-8"))
def moveY(rate):
    ser.write(bytes("moveY {0}".format(rate), "utf-8"))
def moveZ(rate):
    ser.write(bytes("moveZ {0}".format(rate), "utf-8"))
def rot(direction, value):
    ser.write(bytes("rot {0} {1}".format(direction, value), "utf-8"))

init(power_width,power_height,power_push)
time.sleep(direy)
moveX(act_width_s)
time.sleep(direy)
moveY(act_height_s)
time.sleep(direy)

while flag < act_width_f:
    moveY(act_height_f)
    time.sleep(direy)
    moveX(act_width_s + core_width * flag1)
    time.sleep(direy)
    moveY(act_height_s)
    time.sleep(direy)
    moveX(act_width_s + core_width * flag1)
    time.sleep(direy)
    flag1 += 1
    flag += core_width
    

reset()

ser.close()