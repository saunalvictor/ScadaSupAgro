# Local network devices

A network device is a device that will send data to the SCADA server via local network. At the SupAgro Hydraulics hall, the available networks are the WiFi and Ethernet networks, and the WiFi network emitted by the SCADA server which is a Raspberry PI 3 Model B.

The device can be a computer or a microcontroller (Arduino...) with network communication facilities (Ethernet or WiFi shield). It can be connected to one or more sensors (or other data sources) which provides the data to send.

## Declare a new network device

Connect to the SCADA server via telnet and use the `NET` instruction to declare or modify a device.

    NET <DeviceID> <Number of sensors>

In return, the server send an access token. This access token is a secret key that will be used after for sending data to the scada.

Example for declaring a flow-meter which collect one data, type :

    NET FLOWMETER_LIROU 1

The server will respond:

    Network device FLOWMETER_LIROU created with 1 variable(s):
    - FLOWMETER_LIROU_0
    Access token: Sto2aBlhE9rU1l0ogISP

## Send a data to the SCADA

Data are sent by http request. The URL used for sending data should have this format:

    http://SCADA_SERVER:PORT/ACCESS_TOKEN/VALUE1/.../VALUEn

With :

- SCADA_SERVER: Domain name or IP address of SCADA server
- PORT: Server listening port
- ACCESS_TOKEN: the secret key given by the SCADA server for this device
- VALUE1: the first value to send
- VALUEn: the n<sup>th</sup> value to send

Example for the flow-meter created above and a server with the IP address 192.168.200.1 listening on port 34060 sending a discharge of 25.31 L/s:

    http://192.168.200.1:34060/Sto2aBlhE9rU1l0ogISP/25.31

