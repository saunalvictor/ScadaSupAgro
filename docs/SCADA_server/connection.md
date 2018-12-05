# Connection to SCADA server

The server is reachable by telnet protocol on port 443.

Under Linux, use the command line `TELNET 147.99.14.52 443`.

Under Windows, use Putty (<https://portableapps.com/apps/internet/putty_portable>).

![Putty interface](putty.jpg)

- in the field "Host Name (or IP address)", type `147.99.14.52`
- in the field "Port", type `443`
- Choose the protocol "Raw"
- And clic on the "Open" button

The following message should appear on the screen:

    ************************************************************************
    * SupAgro SCADA server v2018                                           *
    * UMR G-EAU, Irstea, SupAgro, David Dorchies, david.dorchies@irstea.fr *
    ************************************************************************

    Connection opened. Please type an instruction or HELP for getting the list of available instructions.

Refer to the [protocol documentation](protocol.md) for interacting with the server.