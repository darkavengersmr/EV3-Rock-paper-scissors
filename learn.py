#!/usr/bin/env python3

from ev3dev.ev3 import *
import pygame
import time
import pygame.camera
from random import random
from PIL import Image, ImageDraw, ImageFont
import datetime

lcd = Screen()
btn = Button()

Sound.play('sound/load.wav').wait()

form = 1
game = 1
ok = 0
ok_all = True

v = 32
g = 24

S1 = TouchSensor("in2")


buf = [ [0] * g for i in range(v)]

class object:
    def __init__(self, n):
        self.name = n
        self.sum = 0
        self.picture = [ [0] * g for i in range(v)]
               
myObject = [object(1), object(2), object(3)]

def image2buf(surf):
    width, height = surf.get_size() 
    for y in range(height): 
        for x in range(width): 
            red, green, blue, alpha = surf.get_at((x, y)) 
            L = 0.3 * red + 0.59 * green + 0.11 * blue
            if L > 70:
                buf[x][y] = 0
            else:
                buf[x][y] = 1
      
pygame.init()
pygame.camera.init()
cameras = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cameras[0])

Sound.play('sound/learnbegin.wav').wait()

while(True):
    lcd.clear()    
    
       
    if(form == 1): Sound.play('sound/move2stone.wav').wait()
    if(form == 2): Sound.play('sound/move2scissors.wav').wait()
    if(form == 3): Sound.play('sound/move2paper.wav').wait()
    
    while(True): 
        if(S1.value()): break   
 
    time.sleep(2)
    
    cam.start()
    image = cam.get_image()
    cam.stop()    

    Sound.beep().wait()    


    image = pygame.transform.scale(image, (v, g))
    image2buf(image)
    
    
    
    for i in range(v):
        for j in range(g):
            if buf[i][j] == 0:
                lcd.draw.rectangle((i*5+9, j*5+4, i*5+4+9, j*5+4+4),fill='white')
            else:
                lcd.draw.rectangle((i*5+9, j*5+4, i*5+4+9, j*5+4+4),fill='black')

    lcd.update()
    
    
    while(True):
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

        a = 0
    
        if(form == 1): 
            if(tmp_obj.name == 1): a = 1
            else: a = -1
        if(form == 2): 
            if(tmp_obj.name == 2): a = 1
            else: a = -1
        if(form == 3): 
            if(tmp_obj.name == 3): a = 1
            else: a = -1
                
        if(a == 1): ok+=1
        if(a == -1): 
            ok=0
            ok_all = False
        for i in range(v):
            for j in range(g):
                if(buf[i][j] == 1):
                    tmp_obj.picture[i][j] += a
   
        print(tmp_obj.name, ok)
        if(ok == 3): 
            form+=1
            if(form == 4): form = 1
            ok = 0
            break
            
    game+=1
    if(game > 9): 
        if(ok_all): break
        else: game-=3
    if(game % 3 == 0): ok_all = True
    
    
Sound.play('sound/saveneural.wav').wait()

    
f = open("kmn_file.txt", "w")
for i in myObject:
    f.write("\n" + str(i.name) + "\n\n")
    for x in range(v):
        for y in range(g):
            f.write(str(i.picture[x][y]) + " ")
        f.write("\n") 
f.close()
Sound.play('sound/learncomplete.wav').wait()


