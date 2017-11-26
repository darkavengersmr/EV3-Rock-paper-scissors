#!/usr/bin/env python3

from ev3dev.ev3 import *
from PIL import Image, ImageDraw, ImageFont
import pygame.camera
import threading
import datetime
import pygame
import random
import time

lcd = Screen()
btn = Button()

Sound.play("sound/load.wav").wait()

lcd.clear()

game = 0

bot_win = 0
man_win = 0

game_itog = 0

roboform = 0

old_man_form = 0

first_game = True

stop = False

v = 32
g = 24

PBC = 5
PA = 5
PD = 10

uA = 0
uB = 0
uC = 0
uD = 0

eA = 0
eB = 0
eC = 0
eD = 0

speedA = 0
speedB = 0
speedC = 0
speedD = 0

speed = 300

S1 = TouchSensor("in2")

A = LargeMotor('outA')
B = LargeMotor('outB')
C = LargeMotor('outC')
D = MediumMotor('outD')

A.reset()
B.reset()
C.reset()
D.reset()

buf = [ [0] * g for i in range(v)]

class object:
    def __init__(self, n):
        self.name = n
        self.sum = 0
        self.picture = [ [0] * g for i in range(v)]
               
myObject = [object(1), object(2), object(3)]

def write(n, m):
    f = ImageFont.truetype('FreeMonoBold.ttf', 155)
    lcd.draw.text((40,-25), str(chr(58)), font=f)

    f = ImageFont.truetype('FreeMonoBold.ttf', 155)
    lcd.draw.text((-10,-10), str(n), font=f)

    f = ImageFont.truetype('FreeMonoBold.ttf', 155)
    lcd.draw.text((95,-10), str(m), font=f)

    lcd.update()

def image2buf(surf):
    width, height = surf.get_size() 
    for y in range(height): 
        for x in range(width): 
            red, green, blue, alpha = surf.get_at((x, y)) 
            L = 0.3 * red + 0.59 * green + 0.11 * blue
            if L > 80:
                buf[x][y] = 0
            else:
                buf[x][y] = 1

def upload_file():
    Sound.play("sound/loadneural.wav").wait()    
    f = open("kmn_file.txt", "r")
    tmp = []
    for i in f:
        tmp.append(i)
    j = 0
    x = 0
    tmpls = ""
    for i in range(len(myObject)):
        j+=3
        for x in range(v):
            tmpls = tmp[j].strip()
            tmpline = tmpls.split()
            j+=1
            for y in range(len(tmpline)-1):
                myObject[i].picture[x][y] = int(tmpline[y])
    f.close()

    for i in myObject:
        for x in range(v):
            for y in range(g):
                print(i.picture[x][y], end=" ")
            print()
        print("\n\n")

def if_form(itog, man_form):
    if(man_form == 1 and itog == 1): return 1
    if(man_form == 2 and itog == 1): return 2
    if(man_form == 3 and itog == 1): return 3

    if(man_form == 1 and itog == 0): return 3
    if(man_form == 2 and itog == 0): return 1
    if(man_form == 3 and itog == 0): return 2


def brake_motor():
    A.stop(stop_action="brake")
    B.stop(stop_action="brake")
    C.stop(stop_action="brake")
    D.stop(stop_action="brake")

def move_hand():
    pos = 30
    while(True):
        if(pos == 0 and not stop): pos = 30
        uA = (pos - A.position)

        speedA = uA*PA
        if(stop):
            pos = 0
            if(abs(uA) < 5): speedA = 0
        if(abs(uA)<5):
            pos *= -1   


        if(speedA > 900): speedA = 900

        if(speedA < -900): speedA = -900

        A.run_forever(speed_sp=speedA)

        time.sleep(0.1)

    brake_motor()
  
def put_form(pB, pC, pD):
    time_start = time.time()
    while(True):
        uB = (pB - B.position)
        uC = (pC - C.position)
        uD = (pD - D.position)
        
        if(abs(uB)<10 and abs(uC)<10 and abs(uD)<15): break 
        
        speedB = uB*PBC
        speedC = uC*PBC
        speedD = uD*PD

        if(time.time() - time_start > 3): break 

        if(speedB > 900): speedB = 900
        if(speedC > 900): speedC = 900
        if(speedD > 900): speedD = 900
         
        if(speedB < -900): speedB = -900
        if(speedC < -900): speedC = -900
        if(speedD < -900): speedD = -900

        B.run_forever(speed_sp=speedB)
        C.run_forever(speed_sp=speedC)
        D.run_forever(speed_sp=speedD)

def put_stone():
    put_form(0, 0, 0)
    brake_motor()
def put_scissors():
    put_form(-160, 0, 0)
    brake_motor()
def put_paper():
    put_form(-160, 160, 0)
    brake_motor()
def put_ok():
    put_form(0, 0, -65)
    brake_motor()



pygame.init()
pygame.camera.init()
cameras = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cameras[0])

upload_file()

stop = True 

move = threading.Thread(target=move_hand)
move.daemon = True
move.start()

Sound.play("sound/rules.wav").wait()

Sound.play("sound/begingame.wav").wait()

while(True):
    time1 = datetime.datetime.now()

    stop = False 

    Sound.play("sound/knb123.wav").wait()

    while(True): 
        cam.start()
        image = cam.get_image()
        cam.stop()

        sum_image = 0

        image = pygame.transform.scale(image, (v, g))
        
        width, height = image.get_size()
        for y in range(height):
            for x in range(width):
                red, green, blue, alpha = image.get_at((x, y))
                L = 0.3 * red + 0.59 * green + 0.11 * blue
                sum_image += L
        print(sum_image/(width*height))
        if(sum_image/(width*height) < 200): 
            break
            Sound.beep()
        if(btn.backspace): 
            brake_motor()
            exit()

    stop = True 
    
    if(not first_game): old_man_form = tmp_obj.name
    
    if(first_game): roboform = int(random.randint(100,399)/100)
    else: roboform = if_form(game_itog, old_man_form)

    game_itog = 0

    if(roboform == 3):
        put_paper()
        Sound.play("sound/paper.wav").wait()
    if(roboform == 1):
        put_stone()
        Sound.play("sound/stone.wav").wait()
    if(roboform == 2):
        put_scissors()
        Sound.play("sound/scissors.wav").wait()

    cam.start()   
    image = cam.get_image()
    cam.stop()   

    Sound.beep().wait()    
    
    image = pygame.transform.scale(image, (v, g))
    image2buf(image)
    
    
    
    for o in myObject:
        o.sum = 0
    for o in myObject:    
        for i in range(v):
            for j in range(g):
                o.sum += buf[i][j] * o.picture[i][j]

    max_sum = -100000
 
    for num in myObject:
        if num.sum > max_sum:
            max_sum = num.sum
            tmp_obj = num
    


    print(bot_win, man_win)

    Sound.play("sound/" + str(tmp_obj.name) + "-" + str(roboform) + ".wav").wait()

    if((tmp_obj.name == 1 and roboform == 2) or (tmp_obj.name == 2 and roboform == 1)): 
        Sound.play("sound/rules12.wav").wait()
    if((tmp_obj.name == 1 and roboform == 3) or (tmp_obj.name == 3 and roboform == 1)):
        Sound.play("sound/rules13.wav").wait()
    if((tmp_obj.name == 2 and roboform == 3) or (tmp_obj.name == 3 and roboform == 2)):
        Sound.play("sound/rules23.wav").wait()

    if(tmp_obj.name == 1):
        if(roboform == 3): 
            Sound.play("sound/ok.wav").wait()
            game_itog = 1
            put_ok()
            game+=1
            bot_win+=1
        elif(roboform == 2): 
            Sound.play("sound/robotlostround1.wav").wait()
            Sound.play("sound/robotlostround2.wav").wait()
            man_win += 1
            game_itog = 0
            game+=1
        else: Sound.play("sound/paritet.wav").wait()
            
    if(tmp_obj.name == 2):
        if(roboform == 1):
            Sound.play("sound/ok.wav").wait()
            game_itog = 1
            put_ok()
            game+=1
            bot_win+=1
        elif(roboform == 3): 
            Sound.play("sound/robotlostround1.wav").wait()
            Sound.play("sound/robotlostround2.wav").wait()
            man_win += 1
            game_itog = 0
            game+=1
        else: Sound.play("sound/paritet.wav").wait()
    if(tmp_obj.name == 3):
        if(roboform == 2):
            Sound.play("sound/ok.wav").wait()
            game_itog = 1
            put_ok()
            game+=1
            bot_win+=1
        elif(roboform == 1): 
            Sound.play("sound/robotlostround1.wav").wait()
            Sound.play("sound/robotlostround2.wav").wait()
            man_win += 1        
            game_itog = 0
            game+=1
        else: Sound.play("sound/paritet.wav").wait()

    lcd.clear()
    write(bot_win, man_win)

    if(game >= 3):
        game = 0
        if(bot_win > man_win): Sound.play("sound/robotwin.wav").wait()
        else: Sound.play("sound/robotlose.wav").wait()
        bot_win = 0
        man_win = 0
    
        lcd.clear()
        write(bot_win, man_win)
    
        print("\n\n\n NEW GAME \n\n\n")
        Sound.play("sound/newgame.wav").wait()

 
    else: Sound.play("sound/newround.wav").wait()

    put_stone()

    time2 = datetime.datetime.now()
    delta = time2-time1
    print(delta.seconds)

    first_game = False

