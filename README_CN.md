DFRobot_BMP150
===========================

* [English Version](./README.md)

BMM150 是一款低功耗、低噪声的 3 轴数字地磁传感器，完全符合罗盘应用的要求。 基于博世专有的 FlipCore 技术，BMM150 提供了高精度和动态的绝对空间方向和运动矢量。 体积小、重量轻，特别适用于支持无人机精准航向。 BMM150 还可与由 3 轴加速度计和 3 轴陀螺仪组成的惯性测量单元一起使用。

![产品效果图](./resources/images/SEN0419-f.png)![产品效果图](./resources/images/SEN0419-b.png)


## 产品链接（[https://www.dfrobot.com.cn/goods-3420.html](https://www.dfrobot.com.cn/goods-3420.html)）
    SKU: SEN0419 
   
## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性)
* [历史](#历史)
* [创作者](#创作者)

## 概述

您可以沿 XYZ 轴获取地磁数据

1. 本模块可以获得高阈值和低阈值地磁数据。 <br>
2. 可以测量三个（xyz）轴上的地磁。<br>
3. 本模块可选择I2C或SPI通讯方式。<br> 

## 库安装

使用此库前，请首先下载库文件，将其粘贴到\Arduino\libraries目录中，然后打开examples文件夹并在该文件夹中运行演示。

## 方法

```C++
  /**
   * @fn softReset
   * @brief 软件复位,软件复位后先恢复为挂起模式,而后恢复为睡眠模式,suspend mode下不能软件复位
   */
  void softReset(void);

  /**
   * @fn setOperationMode
   * @brief 设置传感器的执行模式
   * @param opMode mode
   * @n  BMM150_POWERMODE_NORMAL     normal mode  正常的获得地磁数据的模式
   * @n  BMM150_POWERMODE_FORCED     forced mode  单次测量,测量完成后,传感器恢复sleep mode
   * @n  BMM150_POWERMODE_SLEEP      sleep mode   用户可以访问所有寄存器,不能测量地磁数据
   * @n  BMM150_POWERMODE_SUSPEND    suspend mode 此时传感器cpu不工作,无法执行任何操作,用户只能访问控制寄存器 BMM150_REG_POWER_CONTROL的内容
   */
  void setOperationMode(uint8_t opMode);

  /**
   * @fn getOperationMode
   * @brief 获取传感器的执行模式
   * @return result 返回字符串为传感器的执行模式
   */
  String getOperationMode(void);

  /**
   * @fn setPresetMode
   * @brief 设置预置模式,使用户更简单的配置传感器来获取地磁数据
   * @param presetMode
   * @n BMM150_PRESETMODE_LOWPOWER       低功率模式,获取少量的数据 取均值
   * @n BMM150_PRESETMODE_REGULAR        普通模式,获取中量数据 取均值
   * @n BMM150_PRESETMODE_ENHANCED       增强模式,获取大量数据 取均值
   * @n BMM150_PRESETMODE_HIGHACCURACY   高精度模式,获取超大量数据 取均值
   */
  void setPresetMode(uint8_t presetMode);

  /**
   * @fn setRate
   * @brief 设置获取地磁数据的速率,速率越大获取越快(不加延时函数)
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
   * @brief 获取配置的数据速率 单位：HZ
   * @return rate
   */
  uint8_t getRate(void);

  /**
   * @fn getGeomagneticData
   * @brief 获取x y z 三轴的地磁数据
   * @return 地磁的数据的结构体,单位：微特斯拉（uT）
   */
  sBmm150MagData_t getGeomagneticData(void);

  /**
   * @fn getCompassDegree
   * @brief 获取罗盘方向
   * @return 罗盘方向 (0° - 360°)
   * @n  0° = North, 90° = East, 180° = South, 270° = West.
   */
  float getCompassDegree(void);

  /**
   * @fn setDataReadyPin
   * @brief 使能或者禁止数据准备中断引脚
   * @n 使能后有数据来临DRDY引脚跳变
   * @n 禁止后有数据来临DRDY不进行跳变
   * @n 高极性：高电平为活动电平,默认为低电平,触发中断时电平变为高
   * @n 低极性：低电平为活动电平,默认为高电平,触发中断时电平变为低
   * @param modes
   * @n DRDY_ENABLE        使能DRDY
   * @n DRDY_DISABLE       禁止DRDY
   * @param polarity
   * @n  POLARITY_HIGH      高极性
   * @n  POLARITY_LOW       低极性
   */
  void setDataReadyPin(uint8_t modes, uint8_t polarity=POLARITY_HIGH);

  /**
   * @fn getDataReadyState
   * @brief 获取数据准备的状态,用来判断数据是否准备好
   * @return status
   * @n  true  数据准备好了
   * @n  false 数据没有准备好
   */
  bool getDataReadyState(void);

  /**
   * @fn setMeasurementXYZ
   * @brief 使能x y z 轴的测量,默认设置为使能,禁止后xyz轴的地磁数据不准确
   * @param channelX
   * @n  MEASUREMENT_X_ENABLE        使能 x 轴的测量
   * @n  MEASUREMENT_X_DISABLE       禁止 x 轴的测量
   * @param channelY
   * @n  MEASUREMENT_Y_ENABLE        使能 y 轴的测量
   * @n  MEASUREMENT_Y_DISABLE       禁止 y 轴的测量
   * @param channelZ
   * @n  MEASUREMENT_Z_ENABLE        使能 z 轴的测量
   * @n  MEASUREMENT_Z_DISABLE       禁止 z 轴的测量
   */
  void setMeasurementXYZ(uint8_t channelX = MEASUREMENT_X_ENABLE, uint8_t channelY = MEASUREMENT_Y_ENABLE, uint8_t channelZ = MEASUREMENT_Z_ENABLE);

  /**
   * @fn getMeasurementStateXYZ
   * @brief 获取 x y z 轴的使能状态
   * @return result 返回字符串为使能的状态
   */
  String getMeasurementStateXYZ(void);

  /**
   * @fn setThresholdInterrupt
   * @brief 设置阈值中断,当某个通道的地磁值高/低于阈值时触发中断
   * @n     高极性：高电平为活动电平,默认为低电平,触发中断时电平变为高
   * @n     低极性：低电平为活动电平,默认为高电平,触发中断时电平变为低
   * @param modes
   * @n     LOW_THRESHOLD_INTERRUPT       低阈值中断模式
   * @n     HIGH_THRESHOLD_INTERRUPT      高阈值中断模式
   * @param threshold
   *        阈值,默认扩大16倍,例如：低阈值模式下传入阈值1,实际低于16的地磁数据都会触发中断
   * @param polarity
   * @n     POLARITY_HIGH      高极性
   * @n     POLARITY_LOW       低极性
   */
  void setThresholdInterrupt(uint8_t modes, int8_t threshold, uint8_t polarity);

  /**
   * @fn setThresholdInterrupt
   * @brief 设置阈值中断,当某个通道的地磁值高于/低于阈值时触发中断
   * @n  当产生中断时,INT引脚电平产生跳变
   * @n  高极性：高电平为活动电平,默认为低电平,触发中断时电平变为高
   * @n  低极性：低电平为活动电平,默认为高电平,触发中断时电平变为低
   * @param modes
   * @n     LOW_THRESHOLD_INTERRUPT   低阈值中断模式
   * @n     HIGH_THRESHOLD_INTERRUPT  高阈值中断模式
   * @param channelX
   * @n     INTERRUPT_X_ENABLE        使能 x 轴高阈值中断
   * @n     INTERRUPT_X_DISABLE       禁止 x 轴高阈值中断
   * @param channelY
   * @n     INTERRUPT_Y_ENABLE        使能 y 轴高阈值中断
   * @n     INTERRUPT_Y_DISABLE       禁止 y 轴高阈值中断
   * @param channelZ
   * @n     INTERRUPT_Z_ENABLE        使能 z 轴高阈值中断
   * @n     INTERRUPT_Z_DISABLE       禁止 z 轴高阈值中断
   * @param  threshold
   * @n     阈值,默认扩大16倍,例如：传入 1 的阈值,实际高于/低于16的地磁数据都会触发中断
   * @param polarity
   * @n     POLARITY_HIGH     高极性
   * @n     POLARITY_LOW      低极性
   */
  void setThresholdInterrupt(uint8_t modes, uint8_t channelX, uint8_t channelY, uint8_t channelZ, int8_t threshold, uint8_t polarity);

  /**
   * @fn getThresholdData
   * @brief 获取发生阈值中断的数据
   * @return 返回存放地磁数据的结构体,结构体存放三轴当数据和中断状态,
   * @n xyz轴的数据为 NO_DATA 时,未触发中断
   * @n String state 存放状态二进制数据的字符串
   * @n uint8_t value 存放状态二进制的原始值,数据格式如下
   * @n bit0 is 1 代表x轴发生了中断
   * @n bit1 is 1 代表y轴发生了中断
   * @n bit2 is 1 代表z轴发生了中断
   * @n ------------------------------------
   * @n | bit7 ~ bit3 | bit2 | bit1 | bit0 |
   * @n ------------------------------------
   * @n |  reserved   |  0   |  0   |  0   |
   * @n ------------------------------------
   */
  sBmm150ThresholdData_t getThresholdData(void);

  /**
   * @fn selfTest
   * @brief 传感器自测,返回值表明自检结果
   * @param testMode:
   * @n BMM150_SELF_TEST_NORMAL              // 普通自测,测试X,Y,Z轴是否连接,是否短路
   * @n BMM150_SELF_TEST_ADVANCED            // 高级自测,测试z轴数据的准确性
   * @return result 返回的字符串为自测的结果
   */
  String selfTest(uint8_t testMode);
```

## 兼容性

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | -----
Arduino Uno        |      √       |              |             | 
Mega2560        |      √       |              |             | 
Leonardo        |      √       |              |             | 
ESP32         |      √       |              |             | 
micro:bit        |      √       |              |             | 

## 历史

- 2021/08/16 - 1.0.1 版本
- 2021/04/21 - 1.0.0 版本

## 创作者

Written by ZhixinLiu(zhixin.liu@dfrobot.com), 2021. (Welcome to our [website](https://www.dfrobot.com/))




