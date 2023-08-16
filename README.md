# DFRobot_BMM150

* [中文](./README_CN.md)

The BMM150 is a low-power and low noise 3-axis digital geomagnetic sensor that perfectly matches the requirements of compass applications. Based on Bosch’s proprietary FlipCore technology, the BMM150 provides absolute spatial orientation and motion vectors with high accuracy and dynamics. Featuring small size and lightweight, it is also especially suited for supporting drones in accurate heading. The BMM150 can also be used together with an inertial measurement unit consisting of a 3-axis accelerometer and a 3-axis gyroscope.

![产品效果图](./resources/images/SEN0419-f.png)![产品效果图](./resources/images/SEN0419-b.png)

## Product Link（[https://www.dfrobot.com.cn/](https://www.dfrobot.com.cn/)）
    SKU：SEN0419
    
## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)


## Summary

Get geomagnetic data along the XYZ axis.

1. This module can obtain high threshold and low threshold geomagnetic data. <br>
2. Geomagnetism on three(xyz) axes can be measured.<br>
3. This module can choose I2C or SPI communication mode.<br>

## Installation

To use this library download the zip file, uncompress it to a folder named DFRobot_BMM150.
Download the zip file first to use this library and uncompress it to a folder named DFRobot_BMM150.

## Methods

```C++
  /**
   * @fn softReset
   * @brief Soft reset, restore to suspended mode after soft reset and then enter sleep mode, soft reset can't be implemented under suspend mode
   */
  void softReset(void);

  /**
   * @fn setOperationMode
   * @brief Set sensor operation mode
   * @param opMode mode
   * @n BMM150_POWERMODE_NORMAL      normal mode  Get geomagnetic data normally
   * @n BMM150_POWERMODE_FORCED      forced mode  Single measurement, the sensor restores to sleep mode when the measurement is done.
   * @n BMM150_POWERMODE_SLEEP       sleep mode   Users can visit all the registers, but can’t measure geomagnetic data
   * @n BMM150_POWERMODE_SUSPEND     suspend mode At the time the sensor cpu doesn’t work and can’t implement any operation. Users can only visit the content of the control register BMM150_REG_POWER_CONTROL
   */
  void setOperationMode(uint8_t opMode);

  /**
   * @fn getOperationMode
   * @brief Get sensor operation mode
   * @return result Return sensor operation mode as a character string
   */
  String getOperationMode(void);

  /**
   * @fn setPresetMode
   * @brief Set preset mode, make it easier for users to configure sensor to get geomagnetic data 
   * @param presetMode
   * @n BMM150_PRESETMODE_LOWPOWER       Low power mode, get a fraction of data and take the mean value.
   * @n BMM150_PRESETMODE_REGULAR        Regular mode, get a number of data and take the mean value.
   * @n BMM150_PRESETMODE_ENHANCED       Enhanced mode, get a plenty of data and take the mean value.
   * @n BMM150_PRESETMODE_HIGHACCURACY   High accuracy mode, get a huge number of data and take the mean value.
   */
  void setPresetMode(uint8_t presetMode);

  /**
   * @fn setRate
   * @brief Set the rate of obtaining geomagnetic data, the higher, the faster (without delay function)
   * @param rate
   * @n BMM150_DATA_RATE_02HZ
   * @n BMM150_DATA_RATE_06HZ
   * @n BMM150_DATA_RATE_08HZ
   * @n BMM150_DATA_RATE_10HZ  (default rate)
   * @n BMM150_DATA_RATE_15HZ
   * @n BMM150_DATA_RATE_20HZ
   * @n BMM150_DATA_RATE_25HZ
   * @n BMM150_DATA_RATE_30HZ
   */
  void setRate(uint8_t rate);

  /**
   * @fn getRate
   * @brief Get the config data rate, unit: HZ
   * @return rate
   */
  uint8_t getRate(void);

  /**
   * @fn getGeomagneticData
   * @brief Get the geomagnetic data of 3 axis (x, y, z)
   * @return Geomagnetic data structure, unit: (uT)
   */
  sBmm150MagData_t getGeomagneticData(void);

  /**
   * @fn getCompassDegree
   * @brief Get compass degree
   * @return Compass degree (0° - 360°)
   * @n      0° = North, 90° = East, 180° = South, 270° = West.
   */
  float getCompassDegree(void);

  /**
   * @fn setDataReadyPin
   * @brief Enable or disable data ready interrupt pin
   * @n After enabling, the DRDY pin jump when there's data coming.
   * @n After disabling, the DRDY pin will not jump when there's data coming.
   * @n High polarity: active on high, the default is low level, which turns to high level when the interrupt is triggered.
   * @n Low polarity: active on low, default is high level, which turns to low level when the interrupt is triggered.
   * @param modes
   * @n     DRDY_ENABLE        Enable DRDY
   * @n     DRDY_DISABLE       Disable DRDY
   * @param polarity
   * @n     POLARITY_HIGH      High polarity
   * @n     POLARITY_LOW       Low polarity
   */
  void setDataReadyPin(uint8_t modes, uint8_t polarity=POLARITY_HIGH);

  /**
   * @fn getDataReadyState
   * @brief Get the data ready status, determine whether the data is ready
   * @return status
   * @n true  Data ready
   * @n false Data is not ready
   */
  bool getDataReadyState(void);

  /**
   * @fn setMeasurementXYZ
   * @brief Enable the measurement at x-axis, y-axis and z-axis, default to be enabled. After disabling, the geomagnetic data at x, y, and z axis are wrong.
   * @param channelX
   * @n   MEASUREMENT_X_ENABLE        Enable the measurement at x-axis
   * @n   MEASUREMENT_X_DISABLE       Disable the measurement at x-axis
   * @param channelY
   * @n   MEASUREMENT_Y_ENABLE        Enable the measurement at y-axis
   * @n   MEASUREMENT_Y_DISABLE       Disable the measurement at y-axis
   * @param channelZ
   * @n   MEASUREMENT_Z_ENABLE        Enable the measurement at z-axis
   * @n   MEASUREMENT_Z_DISABLE       Disable the measurement at z-axis
   */
  void setMeasurementXYZ(uint8_t channelX = MEASUREMENT_X_ENABLE, uint8_t channelY = MEASUREMENT_Y_ENABLE, uint8_t channelZ = MEASUREMENT_Z_ENABLE);

  /**
   * @fn getMeasurementStateXYZ
   * @brief Get the enabling status at x-axis, y-axis and z-axis
   * @return result Return enabling status as a character string
   */
  String getMeasurementStateXYZ(void);

  /**
   * @fn setThresholdInterrupt(uint8_t modes, int8_t threshold, uint8_t polarity)
   * @brief Set threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond/below the threshold
   * @n      High polarity: active on high level, the default is low level, which turns to high level when the interrupt is triggered.
   * @n      Low polarity: active on low level, the default is high level, which turns to low level when the interrupt is triggered.
   * @param modes
   * @n     LOW_THRESHOLD_INTERRUPT       Low threshold interrupt mode
   * @n     HIGH_THRESHOLD_INTERRUPT      High threshold interrupt mode
   * @param  threshold
   * @n     Threshold, default to expand 16 times, for example: under low threshold mode, if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
   * @param polarity
   * @n     POLARITY_HIGH      High polarity
   * @n     POLARITY_LOW       Low polarity
   */
  void setThresholdInterrupt(uint8_t modes, int8_t threshold, uint8_t polarity);

  /**
   * @fn setThresholdInterrupt(uint8_t modes, uint8_t channelX, uint8_t channelY, uint8_t channelZ, int8_t threshold, uint8_t polarity)
   * @brief Set threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond/below the threshold
   * @n   When an interrupt occurs, INT pin level will jump
   * @n   High polarity: active on high level, the default is low level, which turns to high level when the interrupt is triggered.
   * @n   Low polarity: active on low level, the default is high level, which turns to low level when the interrupt is triggered.
   * @param modes
   * @n   LOW_THRESHOLD_INTERRUPT   Low threshold interrupt mode
   * @n   HIGH_THRESHOLD_INTERRUPT  High threshold interrupt mode
   * @param channelX
   * @n   INTERRUPT_X_ENABLE        Enable high threshold interrupt at x-axis
   * @n   INTERRUPT_X_DISABLE       Disable high threshold interrupt at x-axis
   * @param channelY
   * @n   INTERRUPT_Y_ENABLE         Enable high threshold interrupt at y-axis
   * @n   INTERRUPT_Y_DISABLE        Disable high threshold interrupt at y-axis
   * @param channelZ
   * @n   INTERRUPT_Z_ENABLE         Enable high threshold interrupt at z-axis
   * @n   INTERRUPT_Z_DISABLE        Disable high threshold interrupt at z-axis
   * @param  threshold
   * @n   Threshold, default to expand 16 times, for example: if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
   * @param polarity
   * @n     POLARITY_HIGH      High polarity
   * @n     POLARITY_LOW       Low polarity
   */
  void setThresholdInterrupt(uint8_t modes, uint8_t channelX, uint8_t channelY, uint8_t channelZ, int8_t threshold, uint8_t polarity);

  /**
   * @fn getThresholdData
   * @brief Get the data with threshold interrupt occurred
   * @return Returns the structure for storing geomagnetic data, the structure stores the data of 3 axis and interrupt status,
   * @n The interrupt is not triggered when the data at x-axis, y-axis and z-axis are NO_DATA
   * @n String state The storage state is binary data string
   * @n uint8_t value The storage state is binary raw value, the data format are as follows:
   * @n bit0 is 1 Indicate the interrupt occur at x-axis
   * @n bit1 is 1 Indicate the interrupt occur at y-axis
   * @n bit2 is 1 Indicate the interrupt occur at z-axis
   * @n ------------------------------------
   * @n | bit7 ~ bit3 | bit2 | bit1 | bit0 |
   * @n ------------------------------------
   * @n |  reserved   |  0   |  0   |  0   |
   * @n ------------------------------------
   */
  sBmm150ThresholdData_t getThresholdData(void);

  /**
   * @fn selfTest
   * @brief The sensor self test, the returned value indicate the self test result.
   * @param testMode:
   * @n    BMM150_SELF_TEST_NORMAL               Normal self test, test whether x-axis, y-axis and z-axis are connected or short-circuited
   * @n    BMM150_SELF_TEST_ADVANCED             Advanced self test, test the data accuracy at z-axis
   * @return result The returned character string is the self test result
   */
  String selfTest(uint8_t testMode);

```
## Compatibility

| MCU                | Work Well | Work Wrong | Untested | Remarks |
| ------------------ | :-------: | :--------: | :------: | ------- |
| Arduino uno        |     √     |            |          |         |
| FireBeetle esp32   |     √     |            |          |         |
| FireBeetle esp8266 |     √     |            |          |         |
| FireBeetle m0      |     √     |            |          |         |
| Leonardo           |     √     |            |          |         |
| Microbit           |     √     |            |          |         |
| Arduino MEGA2560   |     √     |            |          |         |

## History

- 2021/08/16 - Version 1.0.1 released.
- 2021/04/21 - Version 1.0.0 released.

## Credits

Written by ZhixinLiu(zhixin.liu@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))
