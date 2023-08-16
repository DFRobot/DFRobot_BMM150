import sys
import os
import pygame
from pygame.locals import *
import time
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_bmm150 import *

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
  
def loop():
  global previous_angle
  global compass_rect
  global current_angle
  global center_screen_x
  global center_screen_y
  bmm150.get_geomagnetic()
  current_angle = bmm150.get_compass_degree()
  
  events = pygame.event.get()
  for event in events:
    if event.type == QUIT:
        sys.exit()

  if previous_angle != current_angle:
      rotated_compass = pygame.transform.rotate(compass_image,current_angle)
      # compass_pos_x = center_screen_x - (compass_rect.center[0] * 0.5)
      # compass_pos_y = center_screen_y - (compass_rect.center[1] * 0.5)
      compass_pos_x = center_screen_x
      compass_pos_y = center_screen_y
      # print(compass_rect.center)
      compass_rect = rotated_compass.get_rect(center=(compass_pos_x,compass_pos_y))
      surface.fill(BLACK)
      surface.blit(rotated_compass,compass_rect)
      pygame.display.flip()
      previous_angle = current_angle
      # print(current_angle)

  clock.tick(100)


if __name__ == "__main__":
  setup()
  pygame.init()
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  screen_info = pygame.display.Info()
  # WINDOW_SIZE = (screen_info.current_w, screen_info.current_h)
  WINDOW_SIZE = (440, 440)
  surface = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
  pygame.mouse.set_visible(False)
  clock = pygame.time.Clock()
  center_screen_x = int(WINDOW_SIZE[0] * 0.5)
  center_screen_y = int(WINDOW_SIZE[1] * 0.5)
  # set up the colors
  BLACK = (  0,   0,   0)
  WHITE = (255, 255, 255)
  RED   = (255,   0,   0)
  GREEN = (  0, 255,   0)
  BLUE  = (  0,   0, 255)
  #pygame.draw.line(surface, BLUE, (160, 0), (160, 200), 10)
  compass_image = pygame.image.load("compass1.png").convert_alpha()
  compass_rect = compass_image.get_rect()
  previous_angle = 0
  current_angle = 0
  #surface.blit(compass_image,(150,50))

  pygame.display.flip()

  while True:
    loop()
