/*
    Wifi library

    Alexi Husson
    18/04/2019
*/

#include <Arduino.h>

#include "WiFi101.h"

#include "wifi.h"
#include "config.h"

bool wifiConnected() {
  return WiFi.status() == WL_CONNECTED;
}

void printMacAddress() {
  // the MAC address of your Wifi shield
  byte mac[6];

  // print your MAC address:
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5], HEX);
  Serial.print(":");
  Serial.print(mac[4], HEX);
  Serial.print(":");
  Serial.print(mac[3], HEX);
  Serial.print(":");
  Serial.print(mac[2], HEX);
  Serial.print(":");
  Serial.print(mac[1], HEX);
  Serial.print(":");
  Serial.println(mac[0], HEX);
}

void listNetworks() {
  // scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  if (numSsid == -1)
  {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }

  // print the list of networks seen:
  Serial.print("number of available networks:");
  Serial.println(numSsid);

  // print the network number and name for each network found:
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet);
    Serial.print(") ");
    Serial.print(WiFi.SSID(thisNet));
    Serial.print("\tSignal: ");
    Serial.print(WiFi.RSSI(thisNet));
    Serial.print(" dBm");
    Serial.print("\tEncryption: ");
    printEncryptionType(WiFi.encryptionType(thisNet));
    Serial.flush();
  }
}

void printEncryptionType(int thisType) {
  // read the encryption type and print out the name:
  switch (thisType) {
    case ENC_TYPE_WEP:
      Serial.println("WEP");
      break;
    case ENC_TYPE_TKIP:
      Serial.println("WPA");
      break;
    case ENC_TYPE_CCMP:
      Serial.println("WPA2");
      break;
    case ENC_TYPE_NONE:
      Serial.println("None");
      break;
    case ENC_TYPE_AUTO:
      Serial.println("Auto");
      break;
  }
}

void wifiConnect(String ssid, String pass) {
  if ( WiFi.status() != WL_CONNECTED) {
    while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
      digitalWrite(6, HIGH);   // turn the LED on (HIGH is the voltage level)
      listNetworks();
      // unsuccessful, retry in 4 seconds
      Serial.print("failed ... ");
      digitalWrite(6, LOW);    // turn the LED off by making the voltage LOW
      delay(4000);
      Serial.println("retrying ... ");
    }
    Serial.println("connected to Wifi network");
  }
}

bool sendData(String data) {
  WiFiClient client;
  Serial.println("\nStarting connection to server...");
  String str = "GET /" + String(SCADA_TOKEN) + "/" + data;

  if (client.connect(SCADA_SERVER, SCADA_PORT)) {
    Serial.println("connected to server");
    client.println(str);
    client.println("Host: ");
    client.println("Connection: close");
    client.println();
    Serial.println("Data " + str + " sended");
    Serial.println("reponse : ");
    delay(1000);
    while(client.available()) {
      char c = client.read();
      Serial.write(c);
    }
    return true;
  }
  else {
    Serial.println("connection failed");
    WiFi.end();
    return false;
  }
}
