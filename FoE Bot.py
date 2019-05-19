import pyautogui
from time import sleep
from random import randint
import threading
#opencv-python is required! (pip install opencv-python).

#functions to be run, you can change these!
collectGold = True #collect gold from buildings.
collectSupplies = True #collect supplies from buildings.
restartIdleBuildings = True #restart any idle building.
collectGoods = True #collect goods from buildings other than supplies and gold.
pressButtons = True #automatically aid other people and accept friend requests.

#One might need to change these based on screen resolution
ydiff1 = 25
ydiff2 = 50

pyautogui.FAILSAFE = False
lock = threading.Lock()

#Yes I know I'm a crappy programmer.
open("pause.txt", "w+").write("cont")

def processOutput(output):
    #get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    ycoord += ydiff1
    #goto coordinates and click there
    lock.acquire()
    pyautogui.moveTo(xcoord, ycoord, duration=randint(5,15)/10)
    sleep(randint(12,25)/100)
    pyautogui.click()
    pyautogui.moveRel(0, ydiff2, duration=randint(5,15)/20)
    sleep(randint(6,12)/10/7)
    pyautogui.click()
    print("Bot has collected gold from a building.")
    sleep(randint(80,100)/100)
    pyautogui.typewrite(['esc'])
    lock.release()

def processIdleOutput(output):
    #get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    ycoord += ydiff1
    #goto coordinates and click there
    lock.acquire()
    pyautogui.moveTo(xcoord, ycoord, duration=randint(5,15)/10)
    sleep(randint(12,25)/100)
    pyautogui.click()
    sleep(randint(70,90)/100)
    pyautogui.typewrite(['1', '2', '3', '4', '5'])
    pyautogui.moveRel(0, ydiff2, duration=randint(5,15)/20)
    sleep(randint(6,12)/10/7)
    pyautogui.click()
    pyautogui.typewrite(['1', '2', '3', '4', '5'])
    print("Bot has restarted a production building.")
    sleep(randint(80,100)/100)
    pyautogui.typewrite(['esc']) #for some reason [] are required around 'esc' to actually press the ESC button
    lock.release()

def processButtonOutput(output,suppressESC):
    lock.acquire()
    #get coordinates to click from output
    xcoord, ycoord, xcoord2, ycoord2 = output
    #goto coordinates and click there
    pyautogui.moveTo(randint(xcoord+1, xcoord+xcoord2-1), randint(ycoord+1, ycoord+ycoord2-1), duration=randint(5,15)/10)
    sleep(randint(12,25)/100)
    pyautogui.click()
    print("Bot has clicked a button.")
    if suppressESC == False:
        sleep(randint(80,100)/100)
        pyautogui.typewrite(['esc'])
    lock.release()

def worker1(lock): #gold icons
    while True:
        output = pyautogui.locateOnScreen('gold1.png', confidence=0.905)
        lock.acquire()
        print("gold1:", output)
        lock.release()

        if output == None:
            output = pyautogui.locateOnScreen('gold2.png', confidence=0.905)
            lock.acquire()
            print("gold2:", output)
            lock.release()

        if not output == None:
            processOutput(output)
            
def worker2(lock): #supplies icons
    while True:
        output = pyautogui.locateOnScreen('supplies1.png', confidence=0.805)
        lock.acquire()
        print("supplies1:", output)
        lock.release()

        if output== None:
            output = pyautogui.locateOnScreen('supplies2.png', confidence=0.820)
            lock.acquire()
            print("supplies2:", output)
            lock.release()

        if not output == None:
            processOutput(output)
            
def worker3(lock): #idle building icons
    while True:
        output = pyautogui.locateOnScreen('idle1.png', confidence=0.545)
        lock.acquire()
        print("idle1:", output)
        lock.release()
            
        if not output == None:
            processIdleOutput(output)
            
def worker4(lock): #goods boxes icons
    while True:
        output = pyautogui.locateOnScreen('goods1.png', confidence=0.895)
        lock.acquire()
        print("goods1:", output)
        lock.release()
            
        if not output == None:
            processIdleOutput(output)
            
def worker5(lock): #ingame buttons
    suppressESC = False
    while True:
        output = pyautogui.locateOnScreen('button1.png', confidence=0.800, grayscale=True)
        lock.acquire()
        print("button1:", output)
        lock.release()

        if output == None:
            output = pyautogui.locateOnScreen('button2.png', confidence=0.800, grayscale=True)
            lock.acquire()
            print("button2:", output)
            lock.release()
            
        if not output == None:
            processButtonOutput(output, suppressESC)
        else:
            sleep(5)

#multithreading
if collectGold == True:
    t1 = threading.Thread(target=worker1, args=(lock,))
    t1.start()
    
if collectSupplies == True:
    t2 = threading.Thread(target=worker2, args=(lock,))
    t2.start()
    
if restartIdleBuildings == True:
    t3 = threading.Thread(target=worker3, args=(lock,))
    t3.start()

if collectGoods == True:
    t4 = threading.Thread(target=worker4, args=(lock,))
    t4.start()

if pressButtons == True:
    t5 = threading.Thread(target=worker5, args=(lock,))
    t5.start()
        
        
            

