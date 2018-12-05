# Installation of SCADA services on the Raspberry PI


## Install python scripts and dependencies

SCADA services are python script running on the Raspberry PI.

All the script are written in Python 3.

For installing the SCADA services, you should first [open an SSH connection to the Raspberry PI](../Raspberry_PI/ssh.md).

Download the scripts on GitHub with these instructions:

    sudo apt-get install git
    cd /tmp
    git clone https://github.com/DDorch/Scada_DDorch.git
    cp -r Scada_DDorch/server /home/pi/server

Some dependencies should be installed:

    sudo python3 -m pip install http.server
    sudo apt-get install python3-yaml python3-serial

## Configure the python scripts

Copy the file scada_sample.ini to scada.ini :

    cp /home/pi/server/scada_sample.ini /home/pi/server/scada.ini

The configuration of the SCADA is then done by modifying the scada.ini file.

    nano /home/pi/server/scada.ini

## Configure log rotation

Log files are archived by a linux service called logrotate. We should add a configuration file in the folder /etc/logrotate.d in order to take into account the files produced by the SCADA services.

Create a file `/etc/logrotate.d/scada` with this content:

    /var/log/scada/server.log {
        size 1M
        weekly
        rotate 4
        compress
        missingok
        notifempty
        copytruncate
        create 644 root root
    }


## Solve bug of time synchronization

On our Raspbian, the time synchronization didn't work. Since, the Raspberry doesn't have a real time clock, the date and hour are false each time the Raspberry is switched on.

We solve this bug by adding a script with the content below:

    #!/bin/sh
    i=0;while [ $i -lt 100 ]; do i=$(( i+1 ));sleep 1;ping -c1 www.google.com > /dev/null && break; done
    sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

We run it at startup by calling it in `/etc/rc.local` (don't forget to add a `&` at the end of the call - See [this](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md) for details) and we call it once a day by adding a link to this script in the folder `/etc/cron.daily`.


## Install a tool for saving SDD card lifetime

Log2Ram is a tool for writing log files in RAM instead of disk. This can extends consistently the lifetime of the Raspberry SD card.

For installation, follow instructions here : <https://github.com/azlux/log2ram>

By default, log2ram copy the log in the `/var/hdd.log` folder once a day. If you want to copy them once an hour, type the following command:

    sudo mv /etc/cron.hourly/log2ram /etc/cron.daily/log2ram


## Configure startup of the SCADA services

To run the service at startup, add a call to the script `run_scada` in the file `/etc/rc.local`:

    echo "/home/pi/scada/run_scada >> /var/log/scada/run_scada.log" | sudo tee -a etc/rc.local

