#ifndef _WIFI

#define _WIFI
bool wifiConnected();
void printMacAddress();
void listNetworks();
void printEncryptionType(int thisType);
void wifiConnect(String ssid, String pass);
bool sendData(String data);

#endif // _WIFI
