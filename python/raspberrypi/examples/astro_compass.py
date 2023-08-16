import sys
import os
import time
import pygame
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_bmm150 import *

# Initializing Pygame
pygame.init()

I2C_BUS         = 0x01   #default use I2C1
ADDRESS_0       = 0x10   # (CSB:0 SDO:0)
ADDRESS_1       = 0x11   # (CSB:0 SDO:1)
ADDRESS_2       = 0x12   # (CSB:1 SDO:0)
ADDRESS_3       = 0x13   # (CSB:1 SDO:1) default i2c address
bmm150 = DFRobot_bmm150_I2C(I2C_BUS, ADDRESS_3)

def setup():
  while bmm150.ERROR == bmm150.sensor_init():
    print("sensor init error, please check connect") 
    time.sleep(1)
    
  bmm150.set_operation_mode(bmm150.POWERMODE_NORMAL)

  bmm150.set_preset_mode(bmm150.PRESETMODE_HIGHACCURACY)

  bmm150.set_rate(bmm150.RATE_10HZ)

  bmm150.set_measurement_xyz()

# Initialing Color
red = (255,0,0)
back = (64,0,0)

# Initializing screen
screen = pygame.display.set_mode((440,440))
screen.fill(back)
 
# Drawing Circle
pygame.draw.ellipse(screen, red, [20,20,400,400], 3)
pygame.display.flip()
#init old x,y Coordinates
cwxa = 0
cwya=200

#set font north, east ... and print
schrift = pygame.font.SysFont('Arial', 20, True, False)
text = schrift.render("N", True, red)
screen.blit(text, [210, 0])
text = schrift.render("W", True, red)
screen.blit(text, [0, 210])
text = schrift.render("O", True, red)
screen.blit(text, [420, 210])
text = schrift.render("S", True, red)
screen.blit(text, [210,420])

#init trigger for loop
aktiv = True

#font for angle in degrees
schrift = pygame.font.SysFont('Arial', 40, True, False)

setup()

while aktiv:
#delete last angle
    pygame.draw.rect(screen, back, [10,10,100,40])
#get the new angle
    bmm150.get_geomagnetic()
    cwg = float(("{:>3.0f}".format(bmm150.get_compass_degree())))
#output angle
    text = schrift.render(str(cwg), True, red)
    screen.blit(text, [10,10])
#angle in degrees to arcs
    cwb = cwg * math.pi / 180 # sin/cos only in arcs
#calculate x,y from arcs in circle
    cwy = float(("{:>3.0f}".format(190*math.cos(cwb))))
    cwx = float(("{:>3.0f}".format(190*math.sin(cwb))))
#calculate coordinates for the remove line an new line
    pygame.draw.line(screen, back, [cwxa+220, 440-(cwya+220)], [220, 220],5)
    pygame.draw.line(screen, red, [cwx+220,440-(cwy+220)], [220, 220],5)
#safe the old coordinates
    cwxa = cwx
    cwya = cwy
#get the escape
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            aktiv = False   
    time.sleep (.33)
pygame.quit()