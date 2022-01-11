 /*!
  * @file  getAllState.ino
  * @brief Get all the config status, self test status; the sensor turns to sleep mode from normal mode after reset
  * @n Experimental phenomenon: serial print the sensor config information and the self-test information
  * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @license     The MIT License (MIT)
  * @author      ZhixinLiu(zhixin.liu@dfrobot.com)
  * @version     V1.0.0
  * @date        2021-04-21
  * @url         https://github.com/dfrobot/DFRobot_BMM150
  */
#include "DFRobot_BMM150.h"

//When using I2C communication, use the following program to construct an object by DFRobot_BMM150_I2C
/*!
 * @brief Constructor 
 * @param pWire I2C controller
 * @param I2C address
 *        i2c Address select, that CS and SDO pin select 1 or 0 indicates the high or low level. There are 4 combinations: 
 *          I2C_ADDRESS_1 0x10  (CS:0 SDO:0)
 *          I2C_ADDRESS_2 0x11  (CS:0 SDO:1)
 *          I2C_ADDRESS_3 0x12  (CS:1 SDO:0)
 *          I2C_ADDRESS_4 0x13  (CS:1 SDO:1) default i2c address
 */
DFRobot_BMM150_I2C bmm150(&Wire, I2C_ADDRESS_4);

//When using SPI communication, use the following program to construct an object by DFRobot_BMM150_SPI
#if defined(ESP32) || defined(ESP8266)
  #define BMM150_CS D3
#elif defined(__AVR__) || defined(ARDUINO_SAM_ZERO)
  #define BMM150_CS 3
#elif (defined NRF5)
  #define BMM150_CS 2  //The corresponding silkscreen on the development board is the P2
#endif
/*!
 * @brief Constructor 
 * @param cs Chip selection pinChip selection pin
 *        spi Connection method
 *        (SDO<-->MISO)    (SDI<-->MOSI)
 *        (SCK<-->SCK)     (PS<--> GND)
 *        (CS<-->CS customize pin)
 */
//DFRobot_BMM150_SPI bmm150(/*cs = */BMM150_CS);

void setup() 
{
  Serial.begin(115200);
  while(!Serial);
  while(bmm150.begin()){
    Serial.println("bmm150 init failed, Please try again!");
    delay(1000);
  } Serial.println("bmm150 init success!");

  /**!
   * Sensor self test, the returned character string indicates the test result.
   * mode:
   *  BMM150_SELF_TEST_NORMAL              // Normal self test, test whether x-axis, y-axis and z-axis are connected or short-circuited
   *  BMM150_SELF_TEST_ADVANCED            // Advanced self test, test the data accuracy at z-axis
   */
  Serial.println(bmm150.selfTest(BMM150_SELF_TEST_NORMAL));

  /**!
   * Set sensor operation mode
   * opMode:
   *   BMM150_POWERMODE_NORMAL  // normal mode  Get geomagnetic data normally
   *   BMM150_POWERMODE_FORCED  // forced mode  Single measurement, the sensor restores to sleep mode when the measurement is done.
   *   BMM150_POWERMODE_SLEEP   // sleep mode   Users can visit all the registers, but can’t measure geomagnetic data
   *   BMM150_POWERMODE_SUSPEND // suspend mode At the time the sensor cpu doesn't work and can't implement any operation.
   *                                            Users can only visit the content of the control register BMM150_REG_POWER_CONTROL
   */
  bmm150.setOperationMode(BMM150_POWERMODE_NORMAL);

  /**!
   * Set preset mode, make it easier for users to configure sensor to get geomagnetic data
   * presetMode:
   *   BMM150_PRESETMODE_LOWPOWER      // Low power mode, get a fraction of data and take the mean value.
   *   BMM150_PRESETMODE_REGULAR       // Regular mode, get a number of data and take the mean value.
   *   BMM150_PRESETMODE_ENHANCED      // Enhanced mode, get a plenty of data and take the mean value.
   *   BMM150_PRESETMODE_HIGHACCURACY  // High accuracy mode, get a huge number of take and draw the mean value.
   */
  bmm150.setPresetMode(BMM150_PRESETMODE_HIGHACCURACY);

  /**!
   * Set the rate of obtaining geomagnetic data, the higher, the faster(without delay function)
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
  bmm150.setRate(BMM150_DATA_RATE_30HZ);

  /**!
   * Enable the measurement at x-axis, y-axis and z-axis, default to be enabled, no config required, the geomagnetic data at x, y and z will be inaccurate when disabled.
   * Refer to setMeasurementXYZ() function in the .h file if you want to configure more parameters.
   */
  bmm150.setMeasurementXYZ();

  /**!
   * Get the config data rate unit: HZ
   */
  uint8_t rate = bmm150.getRate();
  Serial.print("rate is "); Serial.print(rate); Serial.println(" HZ");
  
  /**!
   * Get the measurement status at x-axis, y-axis and z-axis, return the measurement status as character string
   */
  Serial.println(bmm150.getMeasurementStateXYZ());
  
  /**!
   * Get the sensor operation mode, return the sensor operation status as character string
   */
  Serial.println(bmm150.getOperationMode());
  
  /**!
   * Soft reset, restore to suspend mode after soft reset and then enter sleep mode, soft reset can't be implemented under suspend mode.
   */
  bmm150.softReset();    // After software reset, resume sleep mode (Suspend mode cannot be reset)
}

void loop() 
{
  /**!
   * Get the sensor operation mode, return the sensor operation status as character string
   */
  Serial.println(bmm150.getOperationMode());
  delay(1000);
}
