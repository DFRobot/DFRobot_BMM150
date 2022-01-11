# -*- coding:utf-8 -*-
'''
  @file demo_threshold_interrupt.py
  @brief Set the interrupt to be triggered when beyond/below threshold, when the interrupt at a axis occur, the data will be printed in the serial port.
  @n When the geomagnetic data at 3 axis (x, y, z) beyond/below the set threshold, the data will be printed in the serial port, unit (uT)
  @n Experimental phenomenon: the main controller interrupt will be triggered by level change caused by INT pin interrupt, then the geomagnetic data can be obtained
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  @version     V1.0.0
  @date        2021-04-21
  @get from https://www.dfrobot.com
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

RASPBERR_PIN_INT = 25              #INT Interrupt connection pin, BCM25 i.e. GPIO 6
def setup():
  while bmm150.ERROR == bmm150.sensor_init():
    print("sensor init error ,please check connect") 
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

  '''
    Set threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond/below the threshold
    High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
    Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      modes:
        LOW_THRESHOLD_INTERRUPT       Low threshold interrupt mode, interrupt is triggered when below the threshold
        HIGH_THRESHOLD_INTERRUPT      High threshold interrupt mode, interrupt is triggered when beyond the threshold
      threshold
        Threshold range, default to expand 16 times, for example: under low threshold mode, if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
      polarity:
        POLARITY_HIGH                 High polarity
        POLARITY_LOW                  Low polarity
      View the use method in the readme file if you want to use more configs
  '''
  bmm150.set_threshold_interrupt(bmm150.LOW_THRESHOLD_INTERRUPT, 0, bmm150.POLARITY_LOW)

  GPIO.setmode(GPIO.BCM)
  '''
    Set pin mode, configure input mode,
      pull_up_down=GPIO.PUD_DOWN   When DRDY pin is configured high polarity, RASPBERR_PIN_DRDY pin is configured pull-down input.
      pull_up_down=GPIO.PUD_UP     When DRDY pin is configured low polarity, RASPBERR_PIN_DRDY pin is configured pull-up input.    
  '''
  GPIO.setup(RASPBERR_PIN_INT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
  '''
    Get the data that threshold interrupt occured (get the threshold interrupt status through software)
    That the data at (x, y, z) axis are printed in the serial port indicates threshold interrupt occur at (x, y, z) axis
    Return the list for storing geomagnetic data, how the data at 3 axis influence interrupt status
      [0] The data triggering threshold at x-axis, when the data is NO_DATA, the interrupt is triggered.
      [1] The data triggering threshold at y-axis, when the data is NO_DATA, the interrupt is triggered.
      [2] The data triggering threshold at z-axis, when the data is NO_DATA, the interrupt is triggered.
      [3] The character string storing trigger threshold interrupt status
      [4] The binary data format of storing threshold interrupt status are as follows
      ------------------------------------
      | bit7 ~ bit3 | bit2 | bit1 | bit0 |
      ------------------------------------
      |  reserved   |  0   |  0   |  0   |
      ------------------------------------
  '''
  '''
  threshold_data = bmm150.get_threshold_interrupt_data()
  if threshold_data[0] != NO_DATA:
    print("mag x = %d ut"%threshold_data[0]) 
  if threshold_data[1] != NO_DATA:
    print("mag y = %d ut"%threshold_data[1]) 
  if threshold_data[2] != NO_DATA:
    print("mag z = %d ut"%threshold_data[2]) 
  #print("state is %s"%threshold_data[3]) 
  print("")
  time.sleep(0.1)
  '''
  
  
  '''
    Get interrupt pin INT status, determine whether the data is ready (through hardware)
    That the data at (x, y, z) axis are printed in the serial port indicates threshold interrupt occur at (x, y, z) axis
      status:
        GPIO.LOW    Under low polarity, data ready
        GPIO.HIGH   Under high polarity, data ready
  '''
  if GPIO.input(RASPBERR_PIN_INT) == GPIO.LOW:
    threshold_data = bmm150.get_threshold_interrupt_data()
    if threshold_data[0] != bmm150.NO_DATA:
      print("mag x = %d ut"%threshold_data[0]) 
    if threshold_data[1] != bmm150.NO_DATA:
      print("mag y = %d ut"%threshold_data[1]) 
    if threshold_data[2] != bmm150.NO_DATA:
      print("mag z = %d ut"%threshold_data[2]) 
    #print "state is %s"%threshold_data[3]
    print("") 
    time.sleep(0.1)

if __name__ == "__main__":
  setup()
  while True:
    loop()
