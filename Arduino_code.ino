/*

  Arduino Humidity Sensor

  By Jackson Long, William Harley, David Degman, Oscar Cisneros
  Fall 2019
  ENGR114 


  Code that demonstrates the usage of Adafruit's libaries with the Feather HUZZAH ESP8266 board with the DHT22 sensor to output Humidity and Temperature values.

  Code is based off the example code in the DHT library.



  https://pimylifeup.com/arduino-humidity-sensor-dht22/ 



  Requires the following libraries to be installed.


  DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library

  Adafruit Unified Sensor Library : https://github.com/adafruit/Adafruit_Sensor

  Insert this URl in preferences then install through board manager to use Feather Huzzah ESP8266 board as microcontroller.

    http://arduino.esp8266.com/stable/package_esp8266com_index.json


*/

#include <DHT.h> //Include the DHT library.

#include<Adafruit_Sensor.h>  //Include the Sensor library for adafruit driver

#define dataPin 2 //Define the type data pin

#define DHTType DHT22 //Define the DHT sensor (DHT11, or DHT22)



//Instantiate the dht class with our data pin and DHT type.

DHT dht = DHT(dataPin, DHTType);



void setup() {

  Serial.begin(9600); //Start the serial interface on 9600

    dht.begin();   //Call the begin class in the dht object

}



void loop() {

  delay(1000); // Delay for 1 seconds as the DHT22 sampling rate is 0.5Hz

  

  float h = dht.readHumidity(); //read the humidity from the sensor

  

  float t = dht.readTemperature();  // Read temperature as Celsius (the default), insert true as a parameter for fahrenheit



  // Check for any errors, if there is, display error and restart.

  if (isnan(h) || isnan(t)) {

    Serial.println("Failed to read from the DHT sensor, check wiring.");

    return;

  }

  

  //Print out the humidity and temperature as seperate strings with a space inbetween
  // This seperates the data into seperate values that are indexable

  Serial.print(String(h));

  Serial.print(" ");

  Serial.print(String(t));
 
  //Print new line command

  Serial.println();

}
