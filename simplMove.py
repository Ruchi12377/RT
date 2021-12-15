import morter as m
import time
#port = "COM4"
port = "/dev/cu.usbmodem21201"
m.initialize(port, 100, 75, 20, 9, 1000, 300)
m.init(100, 75, 20)

while True:
    val = input()
    if(val == 'w'):
        m.rot(1, -5)
    elif(val == 's'):
        m.rot(1, 5)
    elif(val == 'a'):
        m.rot(0, -5)
    elif(val == 'd'):
        m.rot(0, 5)
    elif(val == 'e'):
        break

m.dispose()
