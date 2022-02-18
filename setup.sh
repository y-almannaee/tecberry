#!/bin/bash

# This is an install script, run it by invoking 
# sh -xc "$(curl -fsSL https://raw.github.com/y-almannaee/peltier-controller/main/setup.sh)"
# on your Raspberry Pi!

ESC=$(printf '\033') RESET="${ESC}[0m" BLACK="${ESC}[30m" RED="${ESC}[31m"
GREEN="${ESC}[32m" YELLOW="${ESC}[33m" BLUE="${ESC}[34m" MAGENTA="${ESC}[35m"
CYAN="${ESC}[36m" WHITE="${ESC}[37m" DEFAULT="${ESC}[39m"

blue_print() { printf "${BLUE}%s${RESET}\n" "$1"; }
red_print() { printf "${RED}%s${RESET}\n" "$1"; }

echo -ne "Press Ctrl+C to close"

leader_or_follower() {
	echo -ne "
Is this Raspberry Pi a leader or follower?
$(blue_print '1)') Leader
$(blue_print '2)') Follower

Option (1/2): "
	read -r ans
	case $ans in
	1)
		LEADER=1
		;;
	2)
		LEADER=0
		;;
	*)
		leader_or_follower
		;;
	esac
}
leader_or_follower

echo -ne "
A hostname is required for us to display the control information and camera feed.
By default this runs on DuckDNS. You may change this later by editing the docker-compose.yml file.
A hostname may look like peltier.duckdns.org. You may register one at DuckDNS.org.
A token will be of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, and you may find it by logging in to
DuckDNS.org from a web browser and looking for the 'token:' field

Entering these values constitutes accepting the LetsEncrypt TOS (https://letsencrypt.org/repository/) 
"
read -p "Enter the hostname (xxxxx.duckdns.org): " user_hostname
echo -e "\n"
read -p 'Enter the token (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx): ' user_duckdns_token
echo -e "\n"
read -p 'Enter the email SSL certificates will be issued for (xxxx@xxxx.com): ' user_email
echo -e "\n"

[ "$UID" -eq 0 ] || exec sudo sh -c "apt install -y avahi-daemon git python3 python3-pip cron"
[ "$UID" -eq 0 ] || exec sudo sh -c "$(curl -fsSL https://get.docker.com)"
[ "$UID" -eq 0 ] || exec sudo sh -c "pip3 install docker-compose"
[ "$UID" -eq 0 ] || exec sudo sh -c 'curl -o ${PWD}/docker-compose.yml "https://raw.githubusercontent.com/y-almannaee/peltier-controller/main/docker-compose-default.yml"'
[ "$UID" -eq 0 ] || exec sudo sh -c "/usr/local/bin/docker-compose pull"
[ "$UID" -eq 0 ] || exec sudo sh -c "export DUCKDNS_TOKEN=${user_duckdns_token};/usr/bin/docker run goacme/lego --accept-tos --path /home/pi/app_data/ --email ${user_email} --dns duckdns --domains ${user_hostname} --domains *.${user_hostname} run"
[ "$UID" -eq 0 ] || exec sudo sh -c "echo 'USER_HOSTNAME=${user_hostname}\nUSER_EMAIL=${user_email}\nUSER_DUCKDNS_TOKEN=${user_duckdns_token}' > ${PWD}/.env"
[ "$UID" -eq 0 ] || exec sudo sh -c "echo '44 4 * * * root /usr/local/bin/docker-compose up letsencryptgo' > /etc/cron.d/lego-renew"