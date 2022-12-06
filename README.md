![](/landing-src/static/logos/android-chrome-192x192.png)

# TECBERRY - Dockerized Thermal Fatigue Testing Implementation

## About the project

Control and automate Peltier modules for thermal fatigue testing from a Raspberry Pi

## Required items

- 1x Raspberry Pi device
- 6x Peltier Module
  - This project was built using the TEC1-12715

## Setup instructions

For this you will need a Raspberry Pi with a working Raspbian installation. To set the Raspberry Pi up, follow the instructions [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#setting-up-your-raspberry-pi). **When choosing the operating system (OS) in the Raspberry Pi imager it is highly recommended that you press on *Raspberry Pi OS (Other)* and select *Raspberry Pi OS Lite (32-bit)* or *Raspberry Pi OS Lite (64-bit)*** 

1. After first boot, plug the Raspberry Pi into an HDMI-compatible monitor and connect a keyboard. 
2. Log in using the default username `pi` and password `raspberry`.
3. Run the following commands on your Raspberry Pi to use the easy setup script:
```console
pi@raspberrypi:~$ sudo apt update && sudo apt install -y python3 python3-pip
pi@raspberrypi:~$ curl -fsSLO https://bit.ly/tecberry-py && sudo python3 tecberry-py
```
4. Follow the setup instructions to configure your Raspberry Pi
5. You may run the containers using the following command:
```console
pi@RaspberryPiLeader:~$ sudo docker-compose pull && sudo docker-compose up -d
```

## Task list

- [x] Create basic dockerfile
- [x] Create easy setup script
- [x] Create remote administration logic
- [x] Create configurable GPIO logic

## Want to modify the project?

If you would like to contribute to the project or simply modify the code to your liking you may do so by:

1. Opening this repo on Github.com and pressing Fork
2. On your PC you may `git clone your/repo` and work on it, then `git push origin`. You may also edit it in the browser
3. Once you are satisfied with the modified code, on Github.com:
    1. press Settings &#8594; Secrets &#8594; Actions and create a secret titled `DOCKERHUB_TOKEN` and `DOCKERHUB_USERNAME` and populate these with the values you get from hub.docker.com
    2.  press Actions &#8594; CI &#8594; Run Workflow (Enable the workflow if it isn't already enabled)
    3.  once the workflow has finished running (usually takes ~20 mins) your Docker containers will be available on Dockerhub, you may follow the setup instructions above to set them up
4. If you would like to contribute back to this project feel free to open a Pull Request with your modifications, we will get to it in a timely manner