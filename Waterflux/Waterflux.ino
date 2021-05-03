/*
  Waterflux 3100 reader
  for Arduino Mkr 1000

  Alexi Husson
  11/04/2019

*/

#include "wifi.h"
#include "config.h"
#include "inputCapture.h"
#include "arrays.h"

#define DEBUG false // debug mode : sends default values to SCADA
#define PRINT true // Prints output on serial

#define WATERFLUX_PIN 5// Waterflux impulsion output (D-) pin
#define DELAY 1000 // Delay btween 2 sends in ms

#define LED_ON 4
#define LED_WIFI 3
#define LED_SCADA_FAIL 2

// Variables
float freq;     // Frequency of input signal
float flow;     // Mesure of flow in L/s
float mem=0; // Array of 5 last mesures
bool sent;

void setup() {

  Serial.begin(9600);
  Serial.flush();

  pinMode(LED_ON, OUTPUT);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_SCADA_FAIL, OUTPUT);

  captureInit(WATERFLUX_PIN);
  Serial.println("\nWaterflux reading");

  digitalWrite(LED_ON, HIGH);
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_SCADA_FAIL, HIGH);

}

void loop() {

  // Nominal mode : sends true data from sensor

  if (!DEBUG) {

    freq = getFreq();
    flow = freq;      // Flowmeter in mode 1 Hz = 1 l/s

    if (freq > 0 && freq < 100) {
      if (PRINT) {
        Serial.print("Frequency pin 5 : ");
        Serial.print(freq);
        Serial.print(" Hz ");
        Serial.print("Flow pin 5 : ");
        Serial.print(flow);
        Serial.print(" L/s\n");
      }

      // Sending data

      if (!wifiConnected()) {
        digitalWrite(LED_WIFI, LOW);
        wifiConnect(WIFI_SSID, WIFI_PASSWORD);
        digitalWrite(LED_SCADA_FAIL, LOW);
        digitalWrite(LED_WIFI, HIGH);
      }
      
      if(abs(flow-mem)>=0,1) sent = sendData(String(flow));
      mem=flow;



      if (!sent) {
        NVIC_SystemReset();
        digitalWrite(LED_SCADA_FAIL, LOW);
      }


    }
    else {
      if (PRINT) {
        Serial.print("Error - ");
        Serial.print("Frequency : ");
        Serial.print(freq);
        Serial.print(" Hz\n");
      }
    }
  }

  // Debug mode : sends default data (10 L/s)

  else if (DEBUG) {

    Serial.print("DEBUG : ");
    if (!wifiConnected()) wifiConnect(WIFI_SSID, WIFI_PASSWORD);
    sendData("10");
  }

  delay(DELAY);
}
