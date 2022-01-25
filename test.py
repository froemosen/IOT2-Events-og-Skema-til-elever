import time
import os

lastClearTime = int(time.time())

def timeToClear(unix):
    global lastClearTime
    
    if unix > lastClearTime+30: 
        lastClearTime = unix
        return True
    else: 
        return False

while True:
    print("Yallah Yallah")
    if timeToClear(int(time.time())): os.system("cls")
