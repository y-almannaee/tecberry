# Raspberry Pi - Dockerized Peltier Controller

## About the project

Conrol and automate Peltier modules for thermal fatigue testing from a Raspberry Pi

## Required items (incomplete)

- 1x Raspberry Pi device
  - This project was built using the Raspberry Pi 3 Model A+
  - Other single-board computers will work provided that
    - you will modify the software to adjust for the differences
    - they are able to run the Debian-based Linux distribution
    - they can interface using the GPIO pins
    - they have internet connectivity
- 1x Peltier Module
  - This project was built using the TEC1-12715
- 1x Dual Full-Bridge Driver
  - This project was built using the L298N

## Setup instructions

For this you will need a Raspberry Pi with a working Raspbian installation. To set the Raspberry Pi up, follow the instructions [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#setting-up-your-raspberry-pi). **When choosing the operating system (OS) in the Raspberry Pi imager it is highly recommended that you press on *Raspberry Pi OS (Other)* and select *Raspberry Pi OS Lite (32-bit)*** 

1. After first boot, plug the Raspberry Pi into an HDMI-compatible monitor and connect a keyboard. 
2. Log in using the default username `pi` and password `raspberry`.
3. Run the following commands on your Raspberry Pi to update and install several key programs:
```console
raspberrypi:~$ sudo apt update && sudo apt upgrade
raspberrypi:~$ sudo apt install -y avahi-daemon git python3 python3-pip
```
4. To get the Docker environment, run the following:
```console
raspberrypi:~$ curl -sSL https://get.docker.com | sh
raspberrypi:~$ sudo pip3 install docker-compose
```
5. Incomplete
