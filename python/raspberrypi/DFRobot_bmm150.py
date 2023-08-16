# -*- coding: utf-8 -*
'''
  @file DFRobot_bmm150.py
  @note DFRobot_bmm150 Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  version  V1.0.0
  date  2021-04-015
  @url https://github.com/DFRobot/DFRobot_BMM150
'''
import serial
import time
import os
import math

class trim_register:
  def __init__(self):
    self.dig_x1   = 0
    self.dig_y1   = 0
    self.dig_x2   = 0
    self.dig_y2   = 0
    self.dig_z1   = 0
    self.dig_z2   = 0
    self.dig_z3   = 0
    self.dig_z4   = 0
    self.dig_xy1  = 0
    self.dig_xy2  = 0
    self.dig_xyz1 = 0
_trim_data = trim_register()

class geomagnetic_data:
  def __init__(self):
    self.x   = 0
    self.y   = 0
    self.z   = 0
    self.r   = 0
_geomagnetic = geomagnetic_data()

class DFRobot_bmm150(object):
  PI                             = 3.141592653
  I2C_MODE                       = 1
  SPI_MODE                       = 2
  ENABLE_POWER                   = 1
  DISABLE_POWER                  = 0
  POLARITY_HIGH                  = 1
  POLARITY_LOW                   = 0
  ERROR                          = -1
  SELF_TEST_XYZ_FALL             = 0
  SELF_TEST_YZ_FAIL              = 1
  SELF_TEST_XZ_FAIL              = 2
  SELF_TEST_Z_FAIL               = 3
  SELF_TEST_XY_FAIL              = 4
  SELF_TEST_Y_FAIL               = 5
  SELF_TEST_X_FAIL               = 6
  SELF_TEST_XYZ_OK               = 7
  DRDY_ENABLE                    = 1
  DRDY_DISABLE                   = 0
  INTERRUPUT_LATCH_ENABLE        = 1
  INTERRUPUT_LATCH_DISABLE       = 0
  MEASUREMENT_X_ENABLE           = 0
  MEASUREMENT_Y_ENABLE           = 0
  MEASUREMENT_Z_ENABLE           = 0
  MEASUREMENT_X_DISABLE          = 1
  MEASUREMENT_Y_DISABLE          = 1
  MEASUREMENT_Z_DISABLE          = 1
  DATA_OVERRUN_ENABLE            = 1
  DATA_OVERRUN_DISABLE           = 0
  OVERFLOW_INT_ENABLE            = 1
  OVERFLOW_INT_DISABLE           = 0
  INTERRUPT_X_ENABLE             = 0
  INTERRUPT_Y_ENABLE             = 0
  INTERRUPT_Z_ENABLE             = 0
  INTERRUPT_X_DISABLE            = 1
  INTERRUPT_Y_DISABLE            = 1
  INTERRUPT_Z_DISABLE            = 1
  
  CHANNEL_X                      = 1
  CHANNEL_Y                      = 2
  CHANNEL_Z                      = 3
  ENABLE_INTERRUPT_PIN           = 1
  DISABLE_INTERRUPT_PIN          = 0
  POWERMODE_NORMAL               = 0x00
  POWERMODE_FORCED               = 0x01
  POWERMODE_SLEEP                = 0x03
  POWERMODE_SUSPEND              = 0x04
  PRESETMODE_LOWPOWER            = 0x01
  PRESETMODE_REGULAR             = 0x02
  PRESETMODE_HIGHACCURACY        = 0x03
  PRESETMODE_ENHANCED            = 0x04
  REPXY_LOWPOWER                 = 0x01
  REPXY_REGULAR                  = 0x04
  REPXY_ENHANCED                 = 0x07
  REPXY_HIGHACCURACY             = 0x17
  REPZ_LOWPOWER                  = 0x01
  REPZ_REGULAR                   = 0x07
  REPZ_ENHANCED                  = 0x0D
  REPZ_HIGHACCURACY              = 0x29
  CHIP_ID_VALUE                  = 0x32
  CHIP_ID_REGISTER               = 0x40
  REG_DATA_X_LSB                 = 0x42
  REG_DATA_READY_STATUS          = 0x48
  REG_INTERRUPT_STATUS           = 0x4a
  CTRL_POWER_REGISTER            = 0x4b
  MODE_RATE_REGISTER             = 0x4c
  REG_INT_CONFIG                 = 0x4D
  REG_AXES_ENABLE                = 0x4E
  REG_LOW_THRESHOLD              = 0x4F
  REG_HIGH_THRESHOLD             = 0x50
  REG_REP_XY                     = 0x51
  REG_REP_Z                      = 0x52
  RATE_10HZ                      = 0x00        #(default rate)
  RATE_02HZ                      = 0x01
  RATE_06HZ                      = 0x02
  RATE_08HZ                      = 0x03
  RATE_15HZ                      = 0x04
  RATE_20HZ                      = 0x05
  RATE_25HZ                      = 0x06
  RATE_30HZ                      = 0x07
  DIG_X1                         = 0x5D
  DIG_Y1                         = 0x5E
  DIG_Z4_LSB                     = 0x62
  DIG_Z4_MSB                     = 0x63
  DIG_X2                         = 0x64
  DIG_Y2                         = 0x65
  DIG_Z2_LSB                     = 0x68
  DIG_Z2_MSB                     = 0x69
  DIG_Z1_LSB                     = 0x6A
  DIG_Z1_MSB                     = 0x6B
  DIG_XYZ1_LSB                   = 0x6C
  DIG_XYZ1_MSB                   = 0x6D
  DIG_Z3_LSB                     = 0x6E
  DIG_Z3_MSB                     = 0x6F
  DIG_XY2                        = 0x70
  DIG_XY1                        = 0x71
  LOW_THRESHOLD_INTERRUPT        = 0x00
  HIGH_THRESHOLD_INTERRUPT       = 0x01
  NO_DATA                        = -32768
  __txbuf          = [0]          # i2c send buffer
  __threshold_mode = 2
  def __init__(self, bus):
    if bus != 0:
      self.__i2c_spi = self.I2C_MODE
    else:
      self.__i2c_spi = self.SPI_MODE

  def sensor_init(self):
    '''!
      @brief Init bmm150 check whether the chip id is right
      @return 0  is init success
              -1 is init failed
    '''
    self.set_power_bit(self.ENABLE_POWER)
    time.sleep(0.003)
    chip_id = self.get_chip_id()
    if chip_id == self.CHIP_ID_VALUE:
      self.get_trim_data()
      return 0
    else:
      return -1

  
  def get_chip_id(self):
    '''!
      @brief get bmm150 chip id
      @return chip id
    '''
    rslt = self.read_reg(self.CHIP_ID_REGISTER, 1)
    return rslt[0]

  def soft_reset(self):
    '''!
      @brief Soft reset, restore to suspend mode after soft reset and then enter sleep mode, soft reset can't be implemented under suspend mode
    '''
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    self.__txbuf[0] = rslt[0] | 0x82
    self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)

  def self_test(self):
    '''!
      @brief Sensor self test, the returned character string indicate the self test result.
      @return The character string of the test result
    '''
    str1 = ""
    self.set_operation_mode(self.POWERMODE_SLEEP)
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    self.__txbuf[0] == rslt[0] | 0x01
    self.write_reg(self.MODE_RATE_REGISTER, self.__txbuf)
    time.sleep(1)
    rslt = self.read_reg(self.REG_DATA_X_LSB, 5)
    number = (rslt[0]&0x01) | (rslt[2]&0x01)<<1 | (rslt[4]&0x01)<<2
    if (number>>0)&0x01:
      str1 += "x "
    if (number>>1)&0x01:
      str1 += "y "
    if (number>>2)&0x01:
      str1 += "z "
    if number == 0:
      str1 = "xyz aix self test fail"
    else:
      str1 += "aix test success"
    return str1

  def set_power_bit(self, ctrl):
    '''!
      @brief Enable or disable power
      @param ctrl is enable/disable power
      @n DISABLE_POWER is disable power
      @n ENABLE_POWER  is enable power
    '''
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    if ctrl == self.DISABLE_POWER:
      self.__txbuf[0] = rslt[0] & 0xFE
      self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)
    else:
      self.__txbuf[0] = rslt[0] | 0x01
      self.write_reg(self.CTRL_POWER_REGISTER, self.__txbuf)

  def get_power_bit(self):
    '''!
      @brief Get the power state
      @return power state
      @n DISABLE_POWER is disable power
      @n ENABLE_POWER  is enable power
    '''
    rslt = self.read_reg(self.CTRL_POWER_REGISTER, 1)
    return rslt[0]&0x01

  def set_operation_mode(self, modes):
    '''!
      @brief Set sensor operation mode
      @param modes
      @n POWERMODE_NORMAL       normal mode  Get geomagnetic data normally
      @n POWERMODE_FORCED       forced mode  Single measurement, the sensor restores to sleep mode when the measurement is done.
      @n POWERMODE_SLEEP        sleep mode   Users can visit all the registers, but can't measure geomagnetic data
      @n POWERMODE_SUSPEND      suspend mode Users can only visit the content of the control register BMM150_REG_POWER_CONTROL
    '''
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    if modes == self.POWERMODE_NORMAL:
      self.set_power_bit(self.ENABLE_POWER)
      rslt[0] = rslt[0] & 0xf9
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif modes == self.POWERMODE_FORCED:
      rslt[0] = (rslt[0] & 0xf9) | 0x02
      self.set_power_bit(self.ENABLE_POWER)
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif modes == self.POWERMODE_SLEEP:
      self.set_power_bit(self.ENABLE_POWER)
      rslt[0] = (rslt[0] & 0xf9) | 0x04
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    else:
      self.set_power_bit(self.DISABLE_POWER)

  def get_operation_mode(self):
    '''!
      @brief Get sensor operation mode
      @return Return the character string of the operation mode
    '''
    str1 = ""
    if self.get_power_bit() == 0:
      mode = self.POWERMODE_SUSPEND
    else:
      rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
      mode = (rslt[0]&0x06)>>1
    if mode == self.POWERMODE_NORMAL:
      str1 = "normal mode"
    elif mode == self.POWERMODE_SLEEP:
      str1 = "sleep mode"
    elif mode == self.POWERMODE_SUSPEND:
      str1 = "suspend mode"
    else:
      str1 = "forced mode"
    return str1

  def set_rate(self, rates):
    '''!
      @brief Set the rate of obtaining geomagnetic data, the higher, the faster (without delay function)
      @param rates
      @n RATE_02HZ
      @n RATE_06HZ
      @n RATE_08HZ
      @n RATE_10HZ        #(default rate)
      @n RATE_15HZ
      @n RATE_20HZ
      @n RATE_25HZ
      @n RATE_30HZ
    '''
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    if rates == self.RATE_10HZ:
      rslt[0] = rslt[0]&0xc7
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_02HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x08
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_06HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x10
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_08HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x18
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_15HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x20
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_20HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x28
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_25HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x30
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    elif rates == self.RATE_30HZ:
      rslt[0] = (rslt[0]&0xc7) | 0x38
      self.write_reg(self.MODE_RATE_REGISTER, rslt)
    else:
      rslt[0] = rslt[0]&0xc7
      self.write_reg(self.MODE_RATE_REGISTER, rslt)

  def get_rate(self):
    '''!
      @brief Get the config data rate, unit: HZ
      @return rate
    '''
    rslt = self.read_reg(self.MODE_RATE_REGISTER, 1)
    rate = (rslt[0]&0x38)>>3
    if rate == self.RATE_02HZ:
      return 2
    elif rate == self.RATE_06HZ:
      return 6
    elif rate == self.RATE_08HZ:
      return 8
    elif rate == self.RATE_10HZ:
      return 10
    elif rate == self.RATE_15HZ:
      return 15
    elif rate == self.RATE_20HZ:
      return 20
    elif rate == self.RATE_25HZ:
      return 25
    else:
      return 30

  def set_preset_mode(self, modes):
    '''!
      @brief Set preset mode, make it easier for users to configure sensor to get geomagnetic data
      @param modes 
      @n PRESETMODE_LOWPOWER       Low power mode, get a small number of data and take the mean value.
      @n PRESETMODE_REGULAR        Regular mode, get a number of data and take the mean value.
      @n PRESETMODE_ENHANCED       Enhanced mode, get a large number of and take the mean value.
      @n PRESETMODE_HIGHACCURACY   High accuracy mode, get a huge number of data and take the mean value.
    '''
    if modes == self.PRESETMODE_LOWPOWER:
      self.set_xy_rep(self.REPXY_LOWPOWER)
      self.set_z_rep(self.REPZ_LOWPOWER)
    elif modes == self.PRESETMODE_REGULAR:
      self.set_xy_rep(self.REPXY_REGULAR)
      self.set_z_rep(self.REPZ_REGULAR)
    elif modes == self.PRESETMODE_HIGHACCURACY:
      self.set_xy_rep(self.REPXY_HIGHACCURACY)
      self.set_z_rep(self.REPZ_HIGHACCURACY)
    elif modes == self.PRESETMODE_ENHANCED:
      self.set_xy_rep(self.REPXY_ENHANCED)
      self.set_z_rep(self.REPZ_ENHANCED)
    else:
      self.set_xy_rep(self.REPXY_LOWPOWER)
      self.set_z_rep(self.REPZ_LOWPOWER)

  def set_xy_rep(self, modes):
    '''!
      @brief the number of repetitions for x/y-axis
      @param modes
      @n PRESETMODE_LOWPOWER      Low power mode, get the data with lower power.
      @n PRESETMODE_REGULAR       Normal mode, get the data normally
      @n PRESETMODE_HIGHACCURACY  High accuracy mode, get the data with higher accuracy
      @n PRESETMODE_ENHANCED      Enhanced mode, get the data with higher accuracy than under high accuracy mode
    '''
    self.__txbuf[0] = modes
    if modes == self.REPXY_LOWPOWER:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_REGULAR:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_ENHANCED:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    elif modes == self.REPXY_HIGHACCURACY:
      self.write_reg(self.REG_REP_XY, self.__txbuf)
    else:
      self.__txbuf[0] = self.REPXY_LOWPOWER
      self.write_reg(self.REG_REP_XY, self.__txbuf)

  
  def set_z_rep(self, modes):
    '''!
      @brief the number of repetitions for z-axis
      @param modes
      @n PRESETMODE_LOWPOWER      Low power mode, get the data with lower power.
      @n PRESETMODE_REGULAR       Normal mode, get the data normally
      @n PRESETMODE_HIGHACCURACY  High accuracy mode, get the data with higher accuracy
      @n PRESETMODE_ENHANCED      Enhanced mode, get the data with higher accuracy than under high accuracy mode
    '''
    self.__txbuf[0] = modes
    if modes == self.REPZ_LOWPOWER:  
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_REGULAR:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_ENHANCED:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    elif modes == self.REPZ_HIGHACCURACY:
      self.write_reg(self.REG_REP_Z, self.__txbuf)
    else:
      self.__txbuf[0] = self.REPZ_LOWPOWER
      self.write_reg(self.REG_REP_Z, self.__txbuf)

  def get_trim_data(self):
    '''!
      @brief Get bmm150 reserved data information, which is used for data compensation
    '''
    trim_x1_y1    = self.read_reg(self.DIG_X1, 2)
    trim_xyz_data = self.read_reg(self.DIG_Z4_LSB, 4)
    trim_xy1_xy2  = self.read_reg(self.DIG_Z2_LSB, 10)
    _trim_data.dig_x1 = self.uint8_to_int8(trim_x1_y1[0])
    _trim_data.dig_y1 = self.uint8_to_int8(trim_x1_y1[1])
    _trim_data.dig_x2 = self.uint8_to_int8(trim_xyz_data[2])
    _trim_data.dig_y2 = self.uint8_to_int8(trim_xyz_data[3])
    temp_msb = int(trim_xy1_xy2[3]) << 8
    _trim_data.dig_z1 = int(temp_msb | trim_xy1_xy2[2])
    temp_msb = int(trim_xy1_xy2[1] << 8)
    _trim_data.dig_z2 = int(temp_msb | trim_xy1_xy2[0])
    temp_msb = int(trim_xy1_xy2[7] << 8)
    _trim_data.dig_z3 = temp_msb | trim_xy1_xy2[6]
    temp_msb = int(trim_xyz_data[1] << 8)
    _trim_data.dig_z4 = int(temp_msb | trim_xyz_data[0])
    _trim_data.dig_xy1 = trim_xy1_xy2[9]
    _trim_data.dig_xy2 = self.uint8_to_int8(trim_xy1_xy2[8])
    temp_msb = int((trim_xy1_xy2[5] & 0x7F) << 8)
    _trim_data.dig_xyz1 = int(temp_msb | trim_xy1_xy2[4])

  def get_geomagnetic(self):
    '''!
      @brief Get the geomagnetic data of 3 axis (x, y, z)
      @return The list of the geomagnetic data at 3 axis (x, y, z) unit: uT
      @       [0] The geomagnetic data at x-axis
      @       [1] The geomagnetic data at y-axis
      @       [2] The geomagnetic data at z-axis
    '''
    rslt = list(self.read_reg(self.REG_DATA_X_LSB, 8))
    rslt[1] = self.uint8_to_int8(rslt[1])
    rslt[3] = self.uint8_to_int8(rslt[3])
    rslt[5] = self.uint8_to_int8(rslt[5])
    _geomagnetic.x = ((rslt[0]&0xF8) >> 3)  | int(rslt[1]*32)
    _geomagnetic.y = ((rslt[2]&0xF8) >> 3)  | int(rslt[3]*32)
    _geomagnetic.z = ((rslt[4]&0xFE) >> 1)  | int(rslt[5]*128)
    _geomagnetic.r = ((rslt[6]&0xFC) >> 2)  | int(rslt[7]*64)
    rslt[0] = self.compenstate_x(_geomagnetic.x, _geomagnetic.r)
    rslt[1] = self.compenstate_y(_geomagnetic.y, _geomagnetic.r)
    rslt[2] = self.compenstate_z(_geomagnetic.z, _geomagnetic.r)
    return rslt

  def get_f_geomagnetic(self):
    '''!
      @brief Get the geomagnetic data of 3 axis (x, y, z)
      @return The list of the geomagnetic data at 3 axis (x, y, z) unit: uT
      @       [0] The geomagnetic data at x-axis
      @       [1] The geomagnetic data at y-axis
      @       [2] The geomagnetic data at z-axis
    '''
    rslt = self.read_reg(self.REG_DATA_X_LSB, 8)
    rslt[1] = self.uint8_to_int8(rslt[1])
    rslt[3] = self.uint8_to_int8(rslt[3])
    rslt[5] = self.uint8_to_int8(rslt[5])
    _geomagnetic.x = ((rslt[0]&0xF8) >> 3)  | int(rslt[1]*32)
    _geomagnetic.y = ((rslt[2]&0xF8) >> 3)  | int(rslt[3]*32)
    _geomagnetic.z = ((rslt[4]&0xFE) >> 1)  | int(rslt[5]*128)
    _geomagnetic.r = ((rslt[6]&0xFC) >> 2)  | int(rslt[7]*64)
    rslt[0] = self.f_compenstate_x(_geomagnetic.x, _geomagnetic.r)
    rslt[1] = self.f_compenstate_y(_geomagnetic.y, _geomagnetic.r)
    rslt[2] = self.f_compenstate_z(_geomagnetic.z, _geomagnetic.r)
    return rslt
  
  def get_compass_degree(self):
    '''!
      @brief Get compass degree
      @return Compass degree (0° - 360°)  0° = North, 90° = East, 180° = South, 270° = West.
    '''
    geomagnetic = self.get_geomagnetic()
    compass = math.atan2(geomagnetic[0], geomagnetic[1])
    if compass < 0:
      compass += 2 * self.PI
    if compass > 2 * self.PI:
     compass -= 2 * self.PI
    return compass * 180 / self.PI

  def uint8_to_int8(self, number):
    '''!
      @brief uint8_t to int8_t
      @param number    uint8_t data to be transformed
      @return number   The transformed data
    '''
    if number <= 127:
      return number
    else:
      return (256-number)*-1

  def compenstate_x(self, data_x, data_r):
    '''!
      @brief Compensate the geomagnetic data at x-axis
      @param  data_x       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_x != -4096:
      if data_r != 0:
        process_comp_x0 = data_r
      elif _trim_data.dig_xyz1 != 0:
        process_comp_x0 = _trim_data.dig_xyz1
      else:
        process_comp_x0 = 0
      if process_comp_x0 != 0:
        process_comp_x1 = int(_trim_data.dig_xyz1*16384/process_comp_x0)
        process_comp_x2 = int(process_comp_x1 - 0x4000)
        retval = process_comp_x2
        process_comp_x3 = retval*retval
        process_comp_x4 = _trim_data.dig_xy2*(process_comp_x3/128)
        process_comp_x5 = _trim_data.dig_xy1*128
        process_comp_x6 = retval*process_comp_x5
        process_comp_x7 = (process_comp_x4+process_comp_x6)/512 + 0x100000
        process_comp_x8 = _trim_data.dig_x2 + 0xA0
        process_comp_x9 = (process_comp_x8*process_comp_x7)/4096
        process_comp_x10= data_x*process_comp_x9
        retval = process_comp_x10/8192
        retval = (retval + _trim_data.dig_x1*8)/16
      else:
        retval = -32768
    else:
      retval = -32768
    return retval

  def compenstate_y(self, data_y, data_r):
    '''!
      @brief Compensate the geomagnetic data at y-axis
      @param  data_y       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_y != -4096:
      if data_r != 0:
        process_comp_y0 = data_r
      elif _trim_data.dig_xyz1 != 0:
        process_comp_y0 = _trim_data.dig_xyz1
      else:
        process_comp_y0 = 0
      if process_comp_y0 != 0:
        process_comp_y1 = int(_trim_data.dig_xyz1*16384/process_comp_y0)
        process_comp_y2 = int(process_comp_y1 - 0x4000)
        retval = process_comp_y2
        process_comp_y3 = retval*retval
        process_comp_y4 = _trim_data.dig_xy2*(process_comp_y3/128)
        process_comp_y5 = _trim_data.dig_xy1*128
        process_comp_y6 = (process_comp_y4+process_comp_y5*retval)/512
        process_comp_y7 = _trim_data.dig_y2 + 0xA0
        process_comp_y8 = ((process_comp_y6 + 0x100000)*process_comp_y7)/4096
        process_comp_y9 = data_y*process_comp_y8
        retval = process_comp_y9/8192
        retval = (retval + _trim_data.dig_y1*8)/16
      else:
        retval = -32768
    else:
      retval = -32768
    return retval

  def compenstate_z(self, data_z, data_r):
    '''!
      @brief Compensate the geomagnetic data at z-axis
      @param  data_z       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_z != -16384:
      if _trim_data.dig_z2 != 0 and _trim_data.dig_z1 != 0 and _trim_data.dig_xyz1 != 0 and data_r != 0:
        process_comp_z0 = data_r - _trim_data.dig_xyz1
        process_comp_z1 = (_trim_data.dig_z3*process_comp_z0)/4
        process_comp_z2 = (data_z - _trim_data.dig_z4)*32768
        process_comp_z3 = _trim_data.dig_z1 * data_r*2
        process_comp_z4 = (process_comp_z3+32768)/65536
        retval = (process_comp_z2 - process_comp_z1)/(_trim_data.dig_z2+process_comp_z4)
        if retval > 32767:
          retval = 32767
        elif retval < -32767:
          retval = -32767
        retval = retval/16
      else:
        retval = -32768
    else:
      retval = -32768
    return retval

  def f_compenstate_x(self, data_x, data_r):
    '''!
      @brief Compensate the geomagnetic data at x-axis
      @param  data_x       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_x != -4096:
      if _trim_data.dig_xyz1 != 0 and data_r != 0:
        process_comp_x0 = float(_trim_data.dig_xyz1)*16384.0 / float(data_r)
        retval = float(process_comp_x0) - 16384.0
        process_comp_x1 = float(_trim_data.dig_xy2) * float(retval*retval / 268435456.0)
        process_comp_x2 = process_comp_x1 + retval * (float(_trim_data.dig_xy1)/16384.0)
        process_comp_x3 = float(_trim_data.dig_x2) + 160.0
        process_comp_x4 = data_x * ((process_comp_x2 + 256.0) * process_comp_x3)
        retval = (process_comp_x4/8192.0 + (float(_trim_data.dig_x1)*8.0)) / 16.0
      else:
       retval = -32768
    else:
      retval = -32768
    return retval

  def f_compenstate_y(self, data_y, data_r):
    '''!
      @brief Compensate the geomagnetic data at y-axis
      @param  data_y       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_y != -4096:
      if _trim_data.dig_xyz1 != 0 and data_r != 0:
        process_comp_y0 = float(_trim_data.dig_xyz1)*16384.0 / float(data_r)
        retval = float(process_comp_y0) - 16384.0
        process_comp_y1 = float(_trim_data.dig_xy2)* (retval*retval / 268435456.0)
        process_comp_y2 = process_comp_y1 + retval* (float(_trim_data.dig_xy1)/16384.0)
        process_comp_y3 = float(_trim_data.dig_x2) + 160.0
        process_comp_y4 = data_y * ((process_comp_y2 + 256.0) * process_comp_y3)
        retval = (process_comp_y4 / 8192.0 + (float(_trim_data.dig_x1)*8.0))/16.0
      else:
       retval = -32768
    else:
      retval = -32768
    return retval
  def f_compenstate_z(self, data_z, data_r):
    '''!
      @brief Compensate the geomagnetic data at z-axis
      @param  data_z       The raw geomagnetic data
      @param  data_r       The compensated data
      @return retval       The calibrated geomagnetic data
    '''
    if data_z != -16384:
      if _trim_data.dig_z2 != 0 and _trim_data.dig_z1 != 0 and _trim_data.dig_xyz1 != 0 and data_r != 0:
        process_comp_z0 = float(data_z) - float(_trim_data.dig_z4)
        process_comp_z1 = float(data_r) - float(_trim_data.dig_xyz1)
        process_comp_z2 = float(_trim_data.dig_z3) * process_comp_z1
        process_comp_z3 = float(_trim_data.dig_z1) * float(data_r) / 32768.0
        process_comp_z4 = float(_trim_data.dig_z2) + process_comp_z3
        process_comp_z5 = process_comp_z0 * 131072.0 - process_comp_z2
        retval = (process_comp_z5 / (process_comp_z4 * 4.0)) / 16.0
      else:
       retval = -16384
    else:
      retval = -16384
    return retval

  def set_data_ready_pin(self, modes, polarity):
    '''!
      @brief Enable or disable data ready interrupt pin
      @n     After enabling, the pin DRDY signal jump when there's data coming.
      @n     After disabling, the pin DRDY signal does not jump when there's data coming.
      @n     High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
      @n     Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      @param modes
      @n   DRDY_ENABLE      Enable DRDY
      @n   DRDY_DISABLE     Disable DRDY
      @param polarity
      @n   POLARITY_HIGH    High polarity
      @n   POLARITY_LOW     Low polarity
    '''
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.DRDY_DISABLE:
      self.__txbuf[0] = rslt[0] & 0x7F
    else:
      self.__txbuf[0] = rslt[0] | 0x80
    if polarity == self.POLARITY_LOW:
      self.__txbuf[0] = self.__txbuf[0] & 0xFB
    else:
      self.__txbuf[0] = self.__txbuf[0] | 0x04
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  def get_data_ready_state(self):
    '''!
      @brief Get data ready status, determine whether the data is ready
      @return status
      @n 1 is   data is ready
      @n 0 is   data is not ready
    '''
    rslt = self.read_reg(self.REG_DATA_READY_STATUS, 1)
    if (rslt[0]&0x01) != 0:
      return 1
    else:
      return 0

  def set_measurement_xyz(self, channel_x = MEASUREMENT_X_ENABLE, channel_y = MEASUREMENT_Y_ENABLE, channel_z = MEASUREMENT_Z_ENABLE):
    '''!
      @brief Enable the measurement at x-axis, y-axis and z-axis, default to be enabled, no config required. When disabled, the geomagnetic data at x, y, and z will be inaccurate.
      @param channel_x
      @n MEASUREMENT_X_ENABLE     Enable the measurement at x-axis
      @n MEASUREMENT_X_DISABLE    Disable the measurement at x-axis
      @param channel_y
      @n MEASUREMENT_Y_ENABLE     Enable the measurement at y-axis
      @n MEASUREMENT_Y_DISABLE    Disable the measurement at y-axis
      @param channel_z
      @n MEASUREMENT_Z_ENABLE     Enable the measurement at z-axis
      @n MEASUREMENT_Z_DISABLE    Disable the measurement at z-axis
    '''
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if channel_x == self.MEASUREMENT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x08
    else:
      self.__txbuf[0] = rslt[0] & 0xF7

    if channel_y == self.MEASUREMENT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x10
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xEF

    if channel_z == self.MEASUREMENT_Z_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x20
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xDF
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  def get_measurement_xyz_state(self):
    '''!
      @brief Get the enabling status at x-axis, y-axis and z-axis
      @return Return enabling status at x-axis, y-axis and z-axis as a character string
    '''
    str1 = ""
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if (rslt[0]&0x08) == 0:
      str1 += "x "
    if (rslt[0]&0x10) == 0:
      str1 += "y "
    if (rslt[0]&0x20) == 0:
      str1 += "z "
    if str1 == "":
      str1 = "xyz aix not enable"
    else:
      str1 += "aix enable"
    return str1

  def set_interrupt_pin(self, modes, polarity):
    '''!
      @brief Enable or disable INT interrupt pin
      @n     Enabling pin will trigger interrupt pin INT level jump
      @n     After disabling pin, INT interrupt pin will not have level jump
      @n     High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
      @n     Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      @param modes
      @n     ENABLE_INTERRUPT_PIN     Enable interrupt pin
      @n     DISABLE_INTERRUPT_PIN    Disable interrupt pin
      @param polarity
      @n     POLARITY_HIGH            High polarity
      @n     POLARITY_LOW             Low polarity
    '''
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.DISABLE_INTERRUPT_PIN:
      self.__txbuf[0] = rslt[0] & 0xBF
    else:
      self.__txbuf[0] = rslt[0] | 0x40
    if polarity == self.POLARITY_LOW:
      self.__txbuf[0] = self.__txbuf[0] & 0xFE
    else:
      self.__txbuf[0] = self.__txbuf[0] | 0x01
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  
  def set_interruput_latch(self, modes):
    '''!
      @brief Set interrupt latch mode, after enabling interrupt latch, the data can be refreshed only when the BMM150_REG_INTERRUPT_STATUS interrupt status register is read.
      @n   Disable interrupt latch, data update in real-time
      @param modes
      @n  INTERRUPUT_LATCH_ENABLE         Enable interrupt latch
      @n  INTERRUPUT_LATCH_DISABLE        Disable interrupt latch
    '''
    rslt = self.read_reg(self.REG_AXES_ENABLE, 1)
    if modes == self.INTERRUPUT_LATCH_DISABLE:
      self.__txbuf[0] = rslt[0] & 0xFD
    else:
      self.__txbuf[0] = rslt[0] | 0x02
    self.write_reg(self.REG_AXES_ENABLE, self.__txbuf)

  
  def set_threshold_interrupt(self, mode, threshold, polarity, channel_x = INTERRUPT_X_ENABLE, channel_y = INTERRUPT_Y_ENABLE, channel_z = INTERRUPT_Z_ENABLE):
    '''!
      @brief Set threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond/below the threshold
      @n      High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
      @n      Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      @param mode
      @n     LOW_THRESHOLD_INTERRUPT     Low threshold interrupt mode
      @n     HIGH_THRESHOLD_INTERRUPT    High threshold interrupt mode
      @param threshold
      @n Threshold, default to expand 16 times, for example: under low threshold mode, if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
      @param polarity
      @n POLARITY_HIGH               High polarity
      @n POLARITY_LOW                Low polarity
      @param channel_x
      @n INTERRUPT_X_ENABLE          Enable low threshold interrupt at x-axis
      @n INTERRUPT_X_DISABLE         Disable low threshold interrupt at x-axis
      @param channel_y
      @n INTERRUPT_Y_ENABLE          Enable low threshold interrupt at y-axis
      @n INTERRUPT_Y_DISABLE         Disable low threshold interrupt at y-axis
      @param channel_z
      @n INTERRUPT_Z_ENABLE          Enable low threshold interrupt at z-axis
      @n INTERRUPT_Z_DISABLE         Disable low threshold interrupt at z-axis
    '''
    if mode == self.LOW_THRESHOLD_INTERRUPT:
      self.__threshold_mode = self.LOW_THRESHOLD_INTERRUPT
      self.set_low_threshold_interrupt(channel_x, channel_y, channel_z, threshold, polarity)
    else:
      self.__threshold_mode = self.HIGH_THRESHOLD_INTERRUPT
      self.set_high_threshold_interrupt(channel_x, channel_y, channel_z, threshold, polarity)

  def get_threshold_interrupt_data(self):
    '''!
      @brief Get the data that threshold interrupt occured
      @return Return the list for storing geomagnetic data, how the data at 3 axis influence interrupt status,
      @n      [0] The data triggering threshold at x-axis, when the data is NO_DATA, the interrupt is triggered.
      @n      [1] The data triggering threshold at y-axis, when the data is NO_DATA, the interrupt is triggered.
      @n      [2] The data triggering threshold at z-axis, when the data is NO_DATA, the interrupt is triggered.
      @n      [3] The character string storing the trigger threshold interrupt status
      @n      [4] The binary data format of storing threshold interrupt status are as follows
      @n         bit0 is 1 indicate threshold interrupt is triggered at x-axis
      @n         bit1 is 1 indicate threshold interrupt is triggered at y-axis
      @n         bit2 is 1 indicate threshold interrupt is triggered at z-axis
      @n         ------------------------------------
      @n         | bit7 ~ bit3 | bit2 | bit1 | bit0 |
      @n         ------------------------------------
      @n         |  reserved   |  0   |  0   |  0   |
      @n         ------------------------------------
    '''
    data = [0]*10
    str1 = ""
    if self.__threshold_mode == self.LOW_THRESHOLD_INTERRUPT:
      state = self.get_low_threshold_interrupt_state()
    else:
      state = self.get_high_threshold_interrupt_state()
    rslt = self.get_geomagnetic()
    if (state>>0)&0x01:
      data[0] = rslt[0]
      str1 += "X "
    else:
      data[0] = self.NO_DATA
    if (state>>1)&0x01:
      data[1] = rslt[1]
      str1 += "Y "
    else:
      data[1] = self.NO_DATA
    if (state>>2)&0x01:
      data[2] = rslt[2]
      str1 += "Z "
    else:
      data[2] = self.NO_DATA
    if state != 0:
      str1 += " threshold interrupt"
    data[3] = str1
    data[4] = state&0x07
    
    return data
  
  def set_low_threshold_interrupt(self, channel_x, channel_y, channel_z, low_threshold, polarity):
    '''!
      @brief Set low threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is below the low threshold
      @n      High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
      @n      Low polarity: active on low, the default is high level, which turns to low level when the interrupt is triggered.
      @param channel_x
      @n     INTERRUPT_X_ENABLE          Enable low threshold interrupt at x-axis
      @n     INTERRUPT_X_DISABLE         Disable low threshold interrupt at x-axis
      @param channel_y
      @n     INTERRUPT_Y_ENABLE          Enable low threshold interrupt at y-axis
      @n     INTERRUPT_Y_DISABLE         Disable low threshold interrupt at y-axis
      @param channel_z
      @n     INTERRUPT_Z_ENABLE          Enable low threshold interrupt at z-axis
      @n     INTERRUPT_Z_DISABLE         Disable low threshold interrupt at z-axis
      @param low_threshold              Low threshold, default to expand 16 times, for example: if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
      @param polarity
      @n     POLARITY_HIGH                   High polarity
      @n     POLARITY_LOW                    Low polarity
    '''
    if low_threshold < 0:
      self.__txbuf[0] = (low_threshold*-1) | 0x80
    else:
      self.__txbuf[0] = low_threshold
    self.write_reg(self.REG_LOW_THRESHOLD ,self.__txbuf)
    rslt = self.read_reg(self.REG_INT_CONFIG, 1)
    if channel_x == self.INTERRUPT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x01
    else:
      self.__txbuf[0] = rslt[0] & 0xFE
    if channel_y == self.INTERRUPT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x02
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xFC
    if channel_x == self.INTERRUPT_X_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x04
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xFB
    self.write_reg(self.REG_INT_CONFIG ,self.__txbuf)
    self.set_interrupt_pin(self.ENABLE_INTERRUPT_PIN, polarity)

  
  def get_low_threshold_interrupt_state(self):
    '''!
      @brief Get the status of low threshold interrupt, which axis triggered the low threshold interrupt
      @return status The returned number indicate the low threshold interrupt occur at which axis
      @n   bit0 is 1 indicate the interrupt occur at x-axis
      @n   bit1 is 1 indicate the interrupt occur at y-axis
      @n   bit2 is 1 indicate the interrupt occur at z-axis
      @n     ------------------------------------
      @n     | bit7 ~ bit3 | bit2 | bit1 | bit0 |
      @n     ------------------------------------
      @n     |  reserved   |  0   |  0   |  0   |
      @n     ------------------------------------
    '''
    rslt = self.read_reg(self.REG_INTERRUPT_STATUS, 1)
    return rslt[0]&0x07

  def set_high_threshold_interrupt(self, channel_x, channel_y, channel_z, high_threshold, polarity):
    '''!
      @brief Set high threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond the threshold, the threshold is default to expand 16 times
      @n    There will be level change when INT pin interrupt occurred
      @n    High pin polarity: active on high, the default is low level, which will jump when the threshold is triggered.
      @n    Low pin polarity: active on low, the default is high level, which will jump when the threshold is triggered.
      @param channel_x
      @n     INTERRUPT_X_ENABLE          Enable high threshold interrupt at x-axis
      @n     INTERRUPT_X_DISABLE         Disable high threshold interrupt at x-axis
      @param channel_y
      @n     INTERRUPT_Y_ENABLE          Enable high threshold interrupt at y-axis
      @n     INTERRUPT_Y_DISABLE         Disable high threshold interrupt at y-axis
      @param channel_z
      @n     INTERRUPT_Z_ENABLE          Enable high threshold interrupt at z-axis
      @n     INTERRUPT_Z_DISABLE         Disable high threshold interrupt at z-axis
      @param high_threshold              High threshold, default to expand 16 times, for example: if the threshold is set to be 1, actually the geomagnetic data beyond 16 will trigger an interrupt
      @param polarity
      @n     POLARITY_HIGH                   High polarity
      @n     POLARITY_LOW                    Low polarity
    '''
    if high_threshold < 0:
      self.__txbuf[0] = (high_threshold*-1) | 0x80
    else:
      self.__txbuf[0] = high_threshold
    self.write_reg(self.REG_HIGH_THRESHOLD, self.__txbuf)
    rslt = self.read_reg(self.REG_INT_CONFIG, 1)
    if channel_x == self.HIGH_INTERRUPT_X_DISABLE:
      self.__txbuf[0] = rslt[0] | 0x08
    else:
      self.__txbuf[0] = rslt[0] & 0xF7
    if channel_y == self.HIGH_INTERRUPT_Y_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x10
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xEF
    if channel_x == self.HIGH_INTERRUPT_X_DISABLE:
      self.__txbuf[0] = self.__txbuf[0] | 0x20
    else:
      self.__txbuf[0] = self.__txbuf[0] & 0xDf
    
    self.write_reg(self.REG_INT_CONFIG ,self.__txbuf)
    self.set_interrupt_pin(self.ENABLE_INTERRUPT_PIN, polarity)

  def get_high_threshold_interrupt_state(self):
    '''!
      @brief Get the status of high threshold interrupt, which axis triggered the high threshold interrupt
      @return status  The returned number indicate the high threshold interrupt occur at which axis
      @n bit0 is 1 indicate the interrupt occur at x-axis
      @n bit1 is 1 indicate the interrupt occur at y-axis
      @n bit2 is 1 indicate the interrupt occur at z-axis
      @n   ------------------------------------
      @n   | bit7 ~ bit3 | bit2 | bit1 | bit0 |
      @n   ------------------------------------
      @n   |  reserved   |  0   |  0   |  0   |
      @n   ------------------------------------
    '''
    rslt = self.read_reg(self.REG_INTERRUPT_STATUS, 1)
    return (rslt[0]&0x38)>>3


class DFRobot_bmm150_I2C(DFRobot_bmm150):
  '''!
    @brief An example of an i2c interface module
  '''
  def __init__(self, bus, addr):
    self.bus = bus
    self.__addr = addr
    if self.is_raspberrypi():
      import smbus
      self.i2cbus = smbus.SMBus(bus)
    else:
      self.test_platform()
    super(DFRobot_bmm150_I2C, self).__init__(self.bus)

  def is_raspberrypi(self):
    import io
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

  def test_platform(self):
    import re
    import platform
    import subprocess
    where = platform.system()
    if where == "Linux":
        p = subprocess.Popen(['i2cdetect', '-l'], stdout=subprocess.PIPE,)
        for i in range(0, 25):
            line = str(p.stdout.readline())
            s = re.search("i2c-tiny-usb", line)
            if s:
                line = re.split(r'\W+', line)
                bus = int(line[2])
        import smbus
        self.i2cbus = smbus.SMBus(bus)
    elif where == "Windows":
        from i2c_mp_usb import I2C_MP_USB as SMBus
        self.i2cbus = SMBus()
    else:
        print("Platform not supported")  

  def write_reg(self, reg, data):
    '''!
      @brief writes data to a register
      @param reg register address
      @param data written data
    '''
    if type(data) == bytearray:
      data = list(data)
    while 1:
      try:
        self.i2cbus.write_i2c_block_data(self.__addr, reg, data)
        return
      except:
        print("please check connect w!")
        time.sleep(1)
        return
  
  def read_reg(self, reg ,len):
    '''!
      @brief read the data from the register
      @param reg register address
      @param len read data length
    '''
    while 1:
      try:
        rslt = self.i2cbus.read_i2c_block_data(self.__addr, reg, len)
        return rslt
      except:
        time.sleep(1)
        print("please check connect r!")
        
        

class DFRobot_bmm150_SPI(DFRobot_bmm150):
  def __init__(self, cs, bus = 0, dev = 0, speed = 1000000):
    import spidev
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    self.__cs = cs
    GPIO.setup(self.__cs, GPIO.OUT)
    GPIO.output(self.__cs, GPIO.LOW)
    self.__spi = spidev.SpiDev()
    self.__spi.open(bus, dev)
    self.__spi.no_cs = True
    self.__spi.max_speed_hz = speed
    super(DFRobot_bmm150_SPI, self).__init__(0)

  def write_reg(self, reg, data):
    '''!
      @brief writes data to a register
      @param reg register address
      @param data written data
    '''
    GPIO.output(self.__cs, GPIO.LOW)
    reg = reg&0x7F
    self.__spi.writebytes([reg,data[0]])
    GPIO.output(self.__cs, GPIO.HIGH)

  def read_reg(self, reg ,len):
    '''!
      @brief read the data from the register
      @param reg register address
      @param len read data length
    '''
    reg = reg|0x80
    GPIO.output(self.__cs, GPIO.LOW)
    self.__spi.writebytes([reg])
    rslt = self.__spi.readbytes(len)
    GPIO.output(self.__cs, GPIO.HIGH)
    return rslt
