# Controlling the Raspberry PI

## Access via SSH console

On Windows, use Putty (https://portableapps.com/apps/internet/putty_portable) or the Portable console emulator for Windows cmder (http://cmder.net/). On Linux, the openssh-client is normally installed by default.

The IP address of the RPI is 147.99.14.52 and the user name is pi.

For putty, refer to RPI documentation (https://www.raspberrypi.org/documentation/remote-access/ssh/windows.md).

On cmder or on Linux, type:

    ssh pi@147.99.14.52

Accept the proposed certificate and type the password of the pi user.

You're now connected to the RPI like if you use a screen and a keyboard directly connected to the PI.

## Shutdown or reboot the RPI

Before switch off the power supply of the RPI, it's better to properly shutdown the system in order to avoid SD card damages.

Command for shutdown:

    sudo halt

Command for reboot:

    sudo reboot
