![](https://github.com/y-almannaee/peltier-controller/html-src/assets/banner_light.png#gh-light-mode-only) 
![](https://github.com/y-almannaee/peltier-controller/html-src/assets/banner_dark.png#gh-dark-mode-only) 

# Raspberry Pi - Dockerized Peltier Controller

## About the project

Control and automate Peltier modules for thermal fatigue testing from a Raspberry Pi. Built for reliability, using hardware redundancy.

## Required items (incomplete)

- 2x Raspberry Pi device
  - This project was built using the Raspberry Pi 3 Model A+
  - Other single-board computers will work provided that
    - you will modify the software to adjust for the differences
    - they are able to run the Debian-based Linux distribution
    - they can interface using the GPIO pins
    - they have internet connectivity
- ?x Peltier Module
  - This project was built using the TEC1-12715
- 1x Dual Full-Bridge Driver
  - This project was built using the L298N

## Setup instructions

For this you will need a Raspberry Pi with a working Raspbian installation. To set the Raspberry Pi up, follow the instructions [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#setting-up-your-raspberry-pi). **When choosing the operating system (OS) in the Raspberry Pi imager it is highly recommended that you press on *Raspberry Pi OS (Other)* and select *Raspberry Pi OS Lite (32-bit)* or *Raspberry Pi OS Lite (64-bit)*** 

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

## Task list

- [x] Create basic dockerfile
- [ ] Architect the leader-follower application in Python
- [ ] Create Nginx configurations for leader & follower
- [ ] Create remote administration logic
- [ ] Create configurable GPIO logic

## Want to modify the project?

If you would like to contribute to the project or simply modify the code to your liking you may do so by:

1. Opening this repo on Github.com and pressing Fork
2. On your PC you may `git clone your/repo` and work on it, then `git push origin`. You may also edit it in the browser
3. Once you are satisfied with the modified code, on Github.com:
    1. press Settings &#8594; Secrets &#8594; Actions and create a secret titled `DOCKERHUB_TOKEN` and `DOCKERHUB_USERNAME` and populate these with the values you get from hub.docker.com
    2.  press Actions &#8594; CI &#8594; Run Workflow (Enable the workflow if it isn't already enabled)
    3.  once the workflow has finished running (usually takes ~20 mins) your Docker containers will be available on Dockerhub, you may follow the setup instructions above to set them up
4. If you would like to contribute back to this project feel free to open a Pull Request with your modifications, we will get to it in a timely manner

## Useful resources

![](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2012/06/Raspberry-Pi-GPIO-Header-with-Photo.png)

Raspberry Pi 3/4 GPIO Pin Headers, courtesy of www.raspberrypi-spy.co.uk