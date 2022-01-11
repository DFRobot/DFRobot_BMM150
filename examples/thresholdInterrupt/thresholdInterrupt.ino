 /*!
  * @file  thresholdInterrupt.ino
  * @brief Set the interrupt to be triggered when beyond/below threshold, when the interrupt at a axis occur, the relevant data will be printed in the serial port.
  * @n Experimental phenomenon: when the geomagnetic data at 3 axis (x, y, z) beyond/below threshold, serial print the geomagnetic data, unit (uT)
  * @n Experimental phenomenon: the main controller interrupt will be triggered by level change caused by INT pin interrupt, then the geomagnetic data can be obtained
  * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @license     The MIT License (MIT)
  * @author      ZhixinLiu(zhixin.liu@dfrobot.com)
  * @version     V1.0.0
  * @date        2021-04-21
  * @url         https://github.com/DFRobot/DFRobot_BMM150
  */
#include "DFRobot_BMM150.h"

//When using I2C communication, use the following program to construct an object by DFRobot_BMM150_I2C
/*!
 * @brief Constructor 
 * @param pWire I2C controller
 * @param I2C address
 *        i2c Address select, that CS and SDO pin select 1 or 0 indicates the high or low respectively. There are 4 combinations: 
 *          I2C_ADDRESS_1 0x10  (CS:0 SDO:0)
 *          I2C_ADDRESS_2 0x11  (CS:0 SDO:1)
 *          I2C_ADDRESS_3 0x12  (CS:1 SDO:0)
 *          I2C_ADDRESS_4 0x13  (CS:1 SDO:1) default i2c address
 *          INT Connect to the interrupt pin of the main controller
 */
DFRobot_BMM150_I2C bmm150(&Wire, I2C_ADDRESS_4);

//When using SPI communication, use the following program to construct an object by DFRobot_BMM150_SPI
#if defined(ESP32) || defined(ESP8266)
  #define BMM150_CS D3
#elif defined(__AVR__) || defined(ARDUINO_SAM_ZERO)
  #define BMM150_CS 3
#elif (defined NRF5)
  #define BMM150_CS 2  //The corresponding silkscreen on the development board is the pin P2
#endif
/*!
 * @brief Constructor 
 * @param cs Chip selection pinChip selection pin
 *        spi connection method
 *        (SDO<-->MISO)    (SDI<-->MOSI)
 *        (SCK<-->SCK)     (PS<--> GND)
 *        (CS<-->CS customize pin)
 *        (INT<-->pin INT connect to the interrupt pin of the main controller)
 */
//DFRobot_BMM150_SPI bmm150(/*cs = */BMM150_CS);

volatile uint8_t interruptFlag = 0;
void myInterrupt(void)
{
  interruptFlag = 1;    // Interrupt flag
  #if defined(ESP32) || defined(ESP8266) || defined(ARDUINO_SAM_ZERO)
    detachInterrupt(13);   // Detach interrupt
  #else
    detachInterrupt(0);   // Detach interrupt
  #endif
}

void setup() 
{
  Serial.begin(115200);
  while(!Serial);
  while(bmm150.begin()){
    Serial.println("bmm150 init failed, Please try again!");
    delay(1000);
  } Serial.println("bmm150 init success!");

  /**!
   * Set sensor operation mode
   * opMode:
   *   BMM150_POWERMODE_NORMAL  // normal mode  Get geomagnetic data normally
   *   BMM150_POWERMODE_FORCED  // forced mode  Single measurement, the sensor restores to sleep mode when the measurement is done.
   *   BMM150_POWERMODE_SLEEP   // sleep mode   Users can visit all the registers, but can't measure geomagnetic data
   *   BMM150_POWERMODE_SUSPEND // suspend mode At the time the sensor cpu doesn't work and can't implement any operation,
   *                                            Users can only visit the content of the control register BMM150_REG_POWER_CONTROL
   */
  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);

  /**!
   * Set preset mode, make it easier for users to configure sensor to get geomagnetic data
   * presetMode:
   *   BMM150_PRESETMODE_LOWPOWER      // Low power mode, get a small number of data and take the mean value.
   *   BMM150_PRESETMODE_REGULAR       // Regular mode, get a number of data and take the mean value.
   *   BMM150_PRESETMODE_ENHANCED      // Enhanced mode, get a large number of data and take the mean value.
   *   BMM150_PRESETMODE_HIGHACCURACY  // High accuracy mode, get a huge number of data and take the mean value.
   */
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);

  /**!
   * Set the rate of obtaining geomagnetic data, the higher, the faster (without delay function)
   * rate:
   *   BMM150_DATA_RATE_02HZ
   *   BMM150_DATA_RATE_06HZ
   *   BMM150_DATA_RATE_08HZ
   *   BMM150_DATA_RATE_10HZ   (default rate)
   *   BMM150_DATA_RATE_15HZ
   *   BMM150_DATA_RATE_20HZ
   *   BMM150_DATA_RATE_25HZ
   *   BMM150_DATA_RATE_30HZ
   */
  bmm150.setRate(BMM150_DATA_RATE_10HZ);

  /**!
   * Enable the measurement at x-axis, y-axis and z-axis, default to be enabled, no config required, the geomagnetic data at x, y and z will be incorrect when disabled.
   * Refer to setMeasurementXYZ() function in the .h file if you want to configure more parameters.
   */
  bmm150.setMeasurementXYZ();

  /*!
   * Set threshold interrupt, an interrupt is triggered when the geomagnetic value of a channel is beyond/below the threshold
   * High polarity: active on high level, the default is low level, which turns to high level when the interrupt is triggered.
   * Low polarity: active on low level, the default is high level, which turns to low level when the interrupt is triggered.
   * modes:
   *   LOW_THRESHOLD_INTERRUPT      // Low threshold interrupt mode, interrupt is triggered when below the threshold
   *   HIGH_THRESHOLD_INTERRUPT     // High threshold interrupt mode, interrupt is triggered when beyond the threshold
   * threshold  //Threshold range, default to expand 16 times, for example: under low threshold mode, if the threshold is set to be 1, actually the geomagnetic data below 16 will trigger an interrupt
   * polarity:
   *   POLARITY_HIGH     // High polarity
   *   POLARITY_LOW      // Low polarity
   * Refer to setThresholdInterrput() function in the .h file if you want to use more parameters.
   */
  bmm150.setThresholdInterrupt(LOW_THRESHOLD_INTERRUPT, 0, POLARITY_LOW);

#if defined(ESP32) || defined(ESP8266)
  /**!
    Select according to the set DADY pin polarity
      INPUT_PULLUP    // Low polarity, set pin 13 to pull-up input
      INPUT_PULLDOWN  // High polarity, set pin 13 to pull-down input
    interput io
      All pins can be used. Pin 13 is recommended
  */
  pinMode(/*Pin */13 ,INPUT_PULLUP);
  attachInterrupt(/*interput io*/13, myInterrupt, ONLOW);
#elif defined(ARDUINO_SAM_ZERO)
  pinMode(/*Pin */13 ,INPUT_PULLUP);
  attachInterrupt(/*interput io*/13, myInterrupt, LOW);
#else
  /**!    The Correspondence Table of AVR Series Arduino Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------
   * |                                        |    Pin       | 2  | 3  |                   |
   * |    Uno, Nano, Mini, other 328-based    |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  |                   |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 2  | 3  | 21 | 20 | 19 | 18 |
   * |               Mega2560                 |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  | 5  |
   * |-------------------------------------------------------------------------------------|
   * |                                        |    Pin       | 3  | 2  | 0  | 1  | 7  |    |
   * |    Leonardo, other 32u4-based          |--------------------------------------------|
   * |                                        | Interrupt No | 0  | 1  | 2  | 3  | 4  |    |
   * |--------------------------------------------------------------------------------------
   */

  /**!    The Correspondence Table of micro:bit Interrupt Pins And Terminal Numbers
   * ---------------------------------------------------------------------------------------------------------------------------------------------
   * |             micro:bit                       | DigitalPin |P0-P20 can be used as an external interrupt                                     |
   * |  (When using as an external interrupt,      |---------------------------------------------------------------------------------------------|
   * |no need to set it to input mode with pinMode)|Interrupt No|Interrupt number is a pin digital value, such as P0 interrupt number 0, P1 is 1 |
   * |-------------------------------------------------------------------------------------------------------------------------------------------|
   */
  /**!
       Select according to the set DADY pin polarity
      INPUT_PULLUP    // Low polarity, set pin 2 to pull-up input
   */
  pinMode(/*Pin */2 ,INPUT_PULLUP);

  /**!
    Set the pin to interrupt mode
    // Open the external interrupt 0, connect INT1/2 to the digital pin of the main control:
      function
        callback function
      state
        LOW            // When the pin is at low level, the interrupt occur, enter interrupt function
  */
  attachInterrupt(/*Interrupt No*/0, /*function*/myInterrupt ,/*state*/LOW );
#endif

}

void loop() 
{
  /**!
   * Get the data that threshold interrupt occured and interrupt status (get the data ready status through software)
   *    Returns the structure for storing geomagnetic data, the structure stores the data of 3 axis and interrupt status,
   *    No interrupt triggered when the data at x-axis, y-axis and z-axis is NO_DATA
   *    Refer to .h file if you want to check interrupt status.
   */
  /*
  sBmm150ThresholdData_t threshold = bmm150.getThresholdData();
  if(threshold.x != NO_DATA){
    Serial.print("mag x = "); Serial.print(threshold.x); Serial.println(" uT");
  }
  if(threshold.y != NO_DATA){
    Serial.print("mag y = "); Serial.print(threshold.y); Serial.println(" uT");
  }
  if(threshold.z != NO_DATA){
    Serial.print("mag z = "); Serial.print(threshold.z); Serial.println(" uT");
  }
  Serial.println();
  */

  /**!
    When the interrupt occur in INT IO, get the threshold interrupt data (get the threshold interrupt status through hardware)
  */
  if(interruptFlag == 1){
    sBmm150ThresholdData_t threshold = bmm150.getThresholdData();
    if(threshold.x != NO_DATA){
      Serial.print("mag x = "); Serial.print(threshold.x); Serial.println(" uT");
    }
    if(threshold.y != NO_DATA){
      Serial.print("mag y = "); Serial.print(threshold.y); Serial.println(" uT");
    }
    if(threshold.z != NO_DATA){
      Serial.print("mag z = "); Serial.print(threshold.z); Serial.println(" uT");
    }
    Serial.println();
    interruptFlag = 0;
    #if defined(ESP32) || defined(ESP8266)
      attachInterrupt(13, myInterrupt, ONLOW);
    #elif defined(ARDUINO_SAM_ZERO)
      attachInterrupt(13, myInterrupt, LOW);
    #else
      attachInterrupt(0, myInterrupt, LOW);
    #endif
  }
  delay(100);
}
