# -*- coding:utf-8 -*-
'''
  @file demo_data_ready_interrupt.py
  @brief Data ready interrupt, DRDY interrupt will be triggered when the geomagnetic data is ready (the software and hardware can determine whether the interrupt occur)
  @n Experimental phenomenon: serial print the geomagnetic data at x-axis, y-axis and z-axis, unit (uT)
  @n Experimental phenomenon: the main controller interrupt will be triggered by level change caused by DRDY pin interrupt, then the geomagnetic data can be obtained.
  @n Connect the sensor DADY pin to the interrupt pin (RASPBERR_PIN_DRDY) of the main controller
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  @version     V1.0.0
  @date        2021-04-21
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
# I2C Address select, that CS and SDO pin select 1 or 0 indicates the high or low level respectively. There are 4 combinations:
ADDRESS_0       = 0x10   # (CSB:0 SDO:0)
ADDRESS_1       = 0x11   # (CSB:0 SDO:1)
ADDRESS_2       = 0x12   # (CSB:1 SDO:0)
ADDRESS_3       = 0x13   # (CSB:1 SDO:1) default i2c address
bmm150 = DFRobot_bmm150_I2C(I2C_BUS, ADDRESS_3)

RASPBERR_PIN_DRDY = 25              #DRDY Interrupt connect pin, BCM25 i.e. GPIO 6

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
        PRESETMODE_REGULAR        Regular mode, get a number of data and draw the mean value.
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

  '''
    Enable or disable data ready interrupt pin
    After enabling, the pin DRDY signal jump when there's data coming.
    After disabling, the pin DRDY signal does not jump when there's data coming.
    High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
    Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      modes:
        DRDY_ENABLE    Enable DRDY
        DRDY_DISABLE   Disable DRDY
      polarity:
        POKARITY_HIGH  High polarity
        POKARITY_LOW   Low polarity
  '''
  bmm150.set_data_ready_pin(bmm150.DRDY_ENABLE, bmm150.POLARITY_LOW)
  
  GPIO.setmode(GPIO.BCM)
  '''
    Set pin mode, configure input mode,
      pull_up_down=GPIO.PUD_DOWN   When pin DRDY is configured high polarity, pin RASPBERR_PIN_DRDY is configured pull-down input.
      pull_up_down=GPIO.PUD_UP     When pin DRDY is configured low polarity, pin RASPBERR_PIN_DRDY is configured pull-up input.    
  '''
  GPIO.setup(RASPBERR_PIN_DRDY, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
  '''
    Get data ready status, determine whether the data is ready (through software)
      status:
        true    Data ready
        false   Data is not ready yet
  '''
  '''
  if bmm150.get_data_ready_state() == 1:
    rslt = bmm150.get_geomagnetic()
    print("mag x = %d ut"%rslt[0]) 
    print("mag y = %d ut"%rslt[1]) 
    print("mag z = %d ut"%rslt[2]) 
    print("") 
  else:
    time.sleep(0.1)
  '''

  '''
    Get interrupt pin DRDY status, determine whether the data is ready (through hardware)
      status:
        GPIO.LOW    Under low polarity, data ready
        GPIO.HIGH   Under high polarity, data ready
  '''
  if GPIO.input(RASPBERR_PIN_DRDY) == GPIO.LOW:
    if bmm150.get_data_ready_state() == 1:
      rslt = bmm150.get_geomagnetic()
      print("mag x = %d ut"%rslt[0]) 
      print("mag y = %d ut"%rslt[1]) 
      print("mag z = %d ut"%rslt[2]) 
      print("")
  time.sleep(0.1)

if __name__ == "__main__":
  setup()
  while True:
    loop()
