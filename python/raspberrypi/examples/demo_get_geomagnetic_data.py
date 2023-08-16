# -*- coding:utf-8 -*-
'''
  @file demo_get_geomagnetic_data.py
  @brief Get the geomagnetic data at 3 axis (x, y, z), get the compass degree
  @n "Compass Degree", the angle formed when the needle rotates counterclockwise from the current position to the true north
  @n Experimental phenomenon: serial print the geomagnetic data at x-axis, y-axis and z-axis and the angle formed when the needle rotates counterclockwise from the current position to the true north
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  @version     V1.0.0
  @date        2021-04-14
  @url https://github.com/DFRobot/DFRobot_BMM150
'''
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from DFRobot_bmm150 import *

'''
  If you want to use SPI to drive this module, uncomment the codes below, and connect the module with Raspberry Pi via SPI port
  Connect to VCC，GND，SCK，SDO，SDI，CS，PS<-->GND pin
'''
RASPBERRY_PIN_CS =  27              #Chip selection pin when SPI is selected, use BCM coding method, the number is 27, corresponding to pin GPIO2
#bmm150 = DFRobot_bmm150_SPI(RASPBERRY_PIN_CS)

'''
  If you want to use I2C to drive this module, uncomment the codes below, and connect the module with Raspberry Pi via I2C port
  Connect to VCC，GND，SCL，SDA pin
'''
I2C_BUS         = 0x01   #default use I2C1
# I2C address select, that CS and SDO pin select 1 or 0 indicates the high or low level respectively. There are 4 combinations: 
ADDRESS_0       = 0x10   # (CSB:0 SDO:0)
ADDRESS_1       = 0x11   # (CSB:0 SDO:1)
ADDRESS_2       = 0x12   # (CSB:1 SDO:0)
ADDRESS_3       = 0x13   # (CSB:1 SDO:1) default i2c address
bmm150 = DFRobot_bmm150_I2C(I2C_BUS, ADDRESS_3)

def setup():
  while bmm150.ERROR == bmm150.sensor_init():
    print("sensor init error, please check connect") 
    time.sleep(1)

  '''
    Set sensor operation mode
      opMode:
        POWERMODE_NORMAL  Get geomagnetic data normally
        POWERMODE_FORCED  Single measurement, the sensor restores to sleep mode when the measurement is done.
        POWERMODE_SLEEP   Users can visit all the registers, but can't measure geomagnetic data
        POWERMODE_SUSPEND At the time the sensor cpu doesn't work and can't implement any operation. Users can only visit the content of the control register BMM150_REG_POWER_CONTROL
  '''
  bmm150.set_operation_mode(bmm150.POWERMODE_NORMAL)

  '''
    Set preset mode, make it easier for users to configure sensor to get geomagnetic data
      presetMode:
        PRESETMODE_LOWPOWER       Low power mode, get a small number of data and take the mean value.
        PRESETMODE_REGULAR        Regular mode, get a number of data and take the mean value.
        PRESETMODE_ENHANCED       Enhanced mode, get a large number of data and take the mean value.
        PRESETMODE_HIGHACCURACY   High accuracy mode, get a huge number of data and take the mean value.
  '''
  bmm150.set_preset_mode(bmm150.PRESETMODE_HIGHACCURACY)

  '''
    Set the rate of obtaining geomagnetic data, the higher, the faster (without delay function)
      rate:
        RATE_02HZ
        RATE_06HZ
        RATE_08HZ
        RATE_10HZ        #(default rate)
        RATE_15HZ
        RATE_20HZ
        RATE_25HZ
        RATE_30HZ
  '''
  bmm150.set_rate(bmm150.RATE_10HZ)
  
  '''
    Enable the measurement at x-axis, y-axis and z-axis, default to be enabled, no config required. When disabled, the geomagnetic data at x, y, and z will be inaccurate.
    Refer to readme file if you want to configure more parameters.
  '''
  bmm150.set_measurement_xyz()
  
def loop():
  geomagnetic = bmm150.get_geomagnetic()
  print("mag x = %d ut"%geomagnetic[0])
  print("mag y = %d ut"%geomagnetic[1])
  print("mag z = %d ut"%geomagnetic[2])
  # get float type data
  #geomagnetic = bmm150.get_f_geomagnetic()
  #print("---------------------------------")
  #print("mag x = %.2f ut"%geomagnetic[0])
  #print("mag y = %.2f ut"%geomagnetic[1])
  #print("mag z = %.2f ut"%geomagnetic[2])
  degree = bmm150.get_compass_degree()
  print("---------------------------------")
  print("the angle between the pointing direction and north (counterclockwise) is: %.2f "%degree) 
  #print("")
  time.sleep(0.1)

if __name__ == "__main__":
  setup()
  while True:
    loop()
