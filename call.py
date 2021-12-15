import morter as m
import time
m.initialize("COM4", 100, 75, 20, 9, 1000, 300)
print ("initialize")
m.init(100, 75, 20)
print("init")
m.eraser(10, 20, 40, 50)
print("erase")
m.dispose()
