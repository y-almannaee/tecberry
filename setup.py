#!/bin/python3

# This is an install script, run it by invoking
# curl -fsSL https://raw.github.com/y-almannaee/peltier-controller/main/setup.py | sudo python3 -
# on your Raspberry Pi!

import shlex, subprocess, sys, traceback, os


def pip_install(package):
	subprocess.check_call(
		[sys.executable, "-m", "pip", "install", "--upgrade", package],
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)


def run_shell(cmd, success_state="", error_state=""):
	try:
		subprocess.check_call(
			shlex.split(cmd),
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
		print(success_state)
		return 0
	except subprocess.CalledProcessError as error:
		print(error_state)
		traceback.print_exception(error)
		return int(error.returncode)


class con_colors:
	HEADER = "\033[95m"
	OKBLUE = "\033[94m"
	OKCYAN = "\033[96m"
	OKGREEN = "\033[92m"
	WARNING = "\033[93m"
	GRAY = "\033[90m"
	FAIL = "\033[91m"
	ENDC = "\033[0m"
	BOLD = "\033[1m"
	UNDERLINE = "\033[4m"


print(
	f"{con_colors.WARNING}Warning: this script upgrades your Raspberry Pi to the latest version using apt full-upgrade"
)
print(
	f"THIS ACTION MAY REMOVE PACKAGES, USE AT YOUR OWN RISK{con_colors.ENDC}\nPress Ctrl+C to close"
)

input("Press Enter to continue")

print(
	f"""
Is this Raspberry Pi a leader or follower?
{con_colors.OKBLUE} a) {con_colors.ENDC}Leader
{con_colors.OKBLUE} b) {con_colors.ENDC}Follower
{con_colors.GRAY} c) Skip mDNS setup{con_colors.ENDC} 

Option (a/b/c): """,
	end="",
)
while True:
	choice = str(input()).lower()
	if choice is "a":
		host_name = "leader"
	elif choice is "b":
		host_name = "follower_1"
	elif choice is "c":
		break
	else:
		print("Enter a, b, or c")
		continue
	run_shell(f"hostnamectl set-hostname {host_name}")
	run_shell(f"systemctl restart avahi-daemon")
	break


print(
	f"""
A hostname is required for us to display the control information and camera feed on a website.
By default we use DuckDNS as it's a free and easy service. You may change this if you are technically savvy.

A hostname may look like peltier.duckdns.org. You may register one at DuckDNS.org.
A token will be of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, and you may find it by logging in to
DuckDNS.org from a web browser and looking for the 'token:' field

{con_colors.UNDERLINE}Entering these values constitutes the acceptance of LetsEncrypt TOS (https://letsencrypt.org/repository/){con_colors.ENDC}  
"""
)

user_hostname = input("Enter the hostname (xxxxx.duckdns.org): ")
user_duckdns_token = input("Enter the token (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx): ")
user_email = input(
	"Enter the email SSL certificates will be issued for (xxxx@xxxx.com): "
)

with open(f"{os.getcwd()}/.env",'r') as file:
	file.writelines([f"USER_HOSTNAME={user_hostname}",f"USER_EMAIL={user_email}",f"USER_DUCKDNS_TOKEN={user_duckdns_token}"])

run_shell("apt update",f"{con_colors.OKBLUE}Updated package lists")
run_shell("apt full-upgrade -y",f"{con_colors.OKBLUE}Upgraded system")
run_shell("apt install -y avahi-utils avahi-daemon git python3 python3-pip cron",f"{con_colors.OKBLUE}Installed prerequisite programs")
if run_shell("command -v docker",f"{con_colors.OKBLUE}Installing Docker",f"{con_colors.OKBLUE}Docker is already installed, skipping") is 1:
	run_shell("bash -c \"$(curl -fsSL https://get.docker.com)\"")
pip_install("docker-compose")
run_shell(f"mv --backup=t {os.getcwd()}/docker-compose.yml {os.getcwd()}/docker-compose-old.yml")
run_shell(f'bash -c "curl \"https://raw.githubusercontent.com/y-almannaee/peltier-controller/main/docker-compose-default.yml\" > {os.getcwd()}/docker-compose.yml"')
run_shell(f'bash -c "mkdir -p {os.getcwd()}/app_data; chown -R pi:pi {os.getcwd()}/app_data {os.getcwd()}/docker-compose.yml {os.getcwd()}/.env"')
run_shell("/usr/local/bin/docker-compose pull")
run_shell(f"/usr/bin/docker run -e DUCKDNS_TOKEN={user_duckdns_token} -v {os.getcwd()}/app_data:/var/lib goacme/lego --accept-tos --path /var/lib/ --email {user_email} --dns duckdns --domains {user_hostname} --domains *.{user_hostname} run")

with open("/etc/cron.d/lego-renew",'r') as file:
	file.writelines(["echo '44 4 * * * root /usr/local/bin/docker-compose up letsencryptgo"])