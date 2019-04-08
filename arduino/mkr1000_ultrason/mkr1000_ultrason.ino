#include <SPI.h>
#include <WiFi101.h>
#include "config.h"

char DOUT_TRIGGER = 1 ;// Broche TRIGGER
char DIN_ECHO = 2  ; // Broche ECHO

float distance;



void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
//  while (!Serial) {
// wait for serial port to connect. Needed for native USB port only
//  }

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // don't continue:
    while (true);
  }

  // Print WiFi MAC address:
  printMacAddress();

  // put your setup code here, to run once:
  pinMode(DOUT_TRIGGER, OUTPUT);  //Configuration des broches  digitalWrite(TRIGG, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(DIN_ECHO, INPUT);

  // Configure LED
  pinMode(6, OUTPUT);
}

void loop() {
  digitalWrite(6, LOW);    // turn the LED off by making the voltage LOW
  //se reconnecte au raspberry
  if ( WiFi.status() != WL_CONNECTED) wifiConnect(WIFI_SSID, WIFI_PASSWORD);
  digitalWrite(6, HIGH);   // turn the LED on (HIGH is the voltage level)
  distance=getDistance();
  Serial.println("distance="+String(distance));
  sendData();
  delay(1000);
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
float getDistance() {
  // put your main code here, to run repeatedly:
 //boucle
  digitalWrite(DOUT_TRIGGER, LOW);
  delayMicroseconds(2);
  digitalWrite(DOUT_TRIGGER, HIGH);// Lance une mesure de distance en envoyant
  delayMicroseconds(10);  //une impulsion HIGH de 10µs sur la broche TRIGGER
  digitalWrite(DOUT_TRIGGER, LOW);

  // Mesure la durée de l'impulsion sur l'ECHO et converti cette durée en distance en cm
  distance = pulseIn(DIN_ECHO,HIGH)/58.0; //on divise par 58 soit multiplier par la fraction 17/1000 (car le son fait un aller-retour (distance à mesurer x 2 x 10ys) à une vitesse de 34000cm/1000000ys)
  return distance;
}

void sendData(){
  // Initialize the Ethernet client library
  // with the IP address and port of the server
  // that you want to connect to (port 80 is default for HTTP):
  WiFiClient client;
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(SCADA_SERVER, SCADA_PORT)) {
    Serial.println("connected to server");
    // Make a HTTP request:
    //string converti un numérique en chaine de caractère
    client.println("GET /" + String(SCADA_TOKEN) + "/" + String(distance));
    client.println("Host: ");
    client.println("Connection: close");
    client.println();
  }else{
    Serial.println("connection failed");
    WiFi.end();
  }
}
