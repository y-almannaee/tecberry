#!/bin/bash

# This is an install script, run it by invoking
# bash -c "$(curl -fsSL https://raw.github.com/y-almannaee/peltier-controller/main/setup.sh)"
# on your Raspberry Pi!

ESC=$(printf '\033') RESET="${ESC}[0m" BLACK="${ESC}[30m" RED="${ESC}[31m"
GREEN="${ESC}[32m" YELLOW="${ESC}[33m" BLUE="${ESC}[34m" MAGENTA="${ESC}[35m"
CYAN="${ESC}[36m" WHITE="${ESC}[37m" DEFAULT="${ESC}[39m"

blue_print() { printf "${BLUE}%s${RESET}\n" "$1"; }
red_print() { printf "${RED}%s${RESET}\n" "$1"; }

echo "$(red_print 'THIS SCRIPT UPGRADES YOUR RASPBERRY PI TO THE LATEST VERSION USING APT FULL-UPGRADE')
THIS ACTION MAY REMOVE PACKAGES, USE AT YOUR OWN RISK
Press Ctrl+C to close
"

leader_or_follower() {
	echo "
Is this Raspberry Pi a leader or follower?
$(blue_print '1)') Leader
$(blue_print '2)') Follower
$(blue_print '3)') Skip mDNS setup

Option (1/2/3): "
	read -r ans
	case $ans in
	1)
		if ping -c 1 -W 1 "rpileader.local"; then
			echo "$(red_print 'Another Leader Pi was found on the network. Terminating.')"
			exit 1
		else
			echo "Set mdns name to rpileader.local"
			host_name="rpileader"
		fi
		;;
	2)
		for i in {1..5}; do
			if ping -c 1 -W 1 "rpifollower${i}.local"; then
				echo "Found a Follower Pi number ${i}"
			else
				echo "Set mdns name to rpifollower${i}.local"
				host_name="rpifollower${i}"
				break
			fi
		done
		;;
	3)
		return 0
		;;
	*)
		echo "Invalid choice. Enter 1 or 2."
		leader_or_follower
		;;
	esac
	sudo bash -c "echo ${host_name} | tee /etc/hostname"
	sudo bash -c "echo 127.0.1.1 ${host_name} >> /etc/hosts"
	sudo bash -c "hostnamectl set-hostname ${host_name}"
	sudo bash -c "systemctl restart avahi-daemon"
}
leader_or_follower

echo "
A hostname is required for us to display the control information and camera feed on a website.
By default we use DuckDNS as it's a free and easy service. You may change this if you are technically savvy.

A hostname may look like peltier.duckdns.org. You may register one at DuckDNS.org.
A token will be of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, and you may find it by logging in to
DuckDNS.org from a web browser and looking for the 'token:' field

Entering these values constitutes accepting the LetsEncrypt TOS (https://letsencrypt.org/repository/) 
"
read -p "Enter the hostname (xxxxx.duckdns.org): " user_hostname
read -p 'Enter the token (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx): ' user_duckdns_token
read -p 'Enter the email SSL certificates will be issued for (xxxx@xxxx.com): ' user_email
echo ""

sudo bash -c "apt update && apt full-upgrade -y && apt install -y avahi-daemon git python3 python3-pip cron"
if ! [ -x "$(command -v docker)" ]; then
	sudo bash -c "$(curl -fsSL https://get.docker.com)"
fi
sudo bash -c "pip3 install --upgrade docker-compose"
sudo bash -c "echo -e 'USER_HOSTNAME=${user_hostname}\nUSER_EMAIL=${user_email}\nUSER_DUCKDNS_TOKEN=${user_duckdns_token}' > ${PWD}/.env"
sudo bash -c "mv --backup=t ${PWD}/docker-compose.yml ${PWD}/docker-compose-old.yml"
sudo bash -c "curl \"https://raw.githubusercontent.com/y-almannaee/peltier-controller/main/docker-compose-default.yml\" > ${PWD}/docker-compose.yml"
sudo bash -c "mkdir -p ${PWD}/app_data; chown -r pi:pi ${PWD}/app_data ${PWD}/docker-compose.yml ${PWD}/.env"
sudo bash -c "/usr/local/bin/docker-compose pull"
sudo bash -c "export DUCKDNS_TOKEN=${user_duckdns_token};/usr/bin/docker run -e DUCKDNS_TOKEN goacme/lego --accept-tos --path ${PWD}/app_data/ --email ${user_email} --dns duckdns --domains ${user_hostname} --domains *.${user_hostname} run"
sudo bash -c "echo '44 4 * * * root /usr/local/bin/docker-compose up letsencryptgo' > /etc/cron.d/lego-renew"
