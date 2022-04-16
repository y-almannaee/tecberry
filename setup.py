#!/bin/python3

# This is an install script, run it by invoking
# curl -fsSLO https://raw.github.com/y-almannaee/tecberry/main/setup.py && sudo python3 setup.py
# on your Raspberry Pi!

import shlex, subprocess, sys, os, time
from pathlib import Path


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


failure_warning = "Make sure you are connected to the internet, there is enough space on the SD card, and that this script is running with Sudo permissions (sudo python3 ./setup.py)"


def pip_install(package):
	try:
		subprocess.check_call(
			[sys.executable, "-m", "pip", "install", "--upgrade", package],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)
	except subprocess.CalledProcessError as error:
		print(f"{con_colors.FAIL}Unable to install {package}", con_colors.ENDC)
		print(
			f"{con_colors.FAIL}Critical failure has occurred, can't continue{con_colors.ENDC}"
		)
		raise SystemExit()


def run_shell(
	cmd,
	success_state="",
	error_state="",
	critical=False,
	shell=False,
	stdout_to=subprocess.DEVNULL,
):
	cmd = shlex.split(cmd) if not shell else cmd
	try:
		subprocess.check_call(
			cmd, stdout=stdout_to, stderr=subprocess.DEVNULL, shell=shell
		)
		print(success_state, con_colors.ENDC)
		return 0
	except subprocess.CalledProcessError as error:
		print(error_state, con_colors.ENDC)
		if critical:
			print(
				f"{con_colors.FAIL}Critical failure has occurred, can't continue{con_colors.ENDC}"
			)
			raise SystemExit()
		return int(error.returncode)


def set_hostname(hostname):
	with open("/etc/hostname", "w") as file:
		file.write(hostname)
	with open("/etc/hosts", "r") as file:
		hosts_file_old = file.readlines()
	hosts_file = []
	for line in hosts_file_old:
		if "127.0.1.1" not in line:
			hosts_file.append(line)
	hosts_file.append(f"127.0.1.1 {hostname}\n")
	with open("/etc/hosts", "w") as file:
		file.writelines(hosts_file)
	run_shell(
		f"hostnamectl set-hostname {hostname}",
		f"{con_colors.OKCYAN}Changed hostname to {hostname}",
		f"{con_colors.FAIL}Could not change hostname to {hostname}. {failure_warning}",
		True,
	)
	run_shell(
		f"systemctl restart avahi-daemon",
		f"{con_colors.OKCYAN}Restarted the mDNS daemon to apply changes",
		f"{con_colors.FAIL}Unable to restartthe mDNS daemon. {failure_warning}",
		True,
	)
	time.sleep(5)


def handle_hostname(choice):
	run_shell(
		"apt update",
		f"{con_colors.OKCYAN}Updated package lists",
		f"{con_colors.FAIL}Can't update package lists. {failure_warning}",
		True,
	)
	run_shell(
		"apt install -y avahi-utils",
		f"{con_colors.OKCYAN}Installed prerequisite programs",
		f"{con_colors.FAIL}Could not install prerequisite programs. {failure_warning}",
		True,
	)
	import socket

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		s.connect(("10.255.255.255", 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = "127.0.0.1"
	finally:
		s.close()
	if choice == 1:
		set_hostname("RaspberryPiLeader")
		out = (
			subprocess.check_output(shlex.split(f"avahi-resolve -a {IP}"))
			.decode()
			.split("\t")[1]
			.strip()
			.split(".")[0]
		)
		if out != "RaspberryPiLeader":
			print(
				f"{con_colors.FAIL}This isn't the only RaspberryPi Leader on the network. Can't continue{con_colors.ENDC}"
			)
			raise SystemExit()
		else:
			return
	else:
		for i in range(1, 4):
			set_hostname(f"RaspberryPiFollower{i}")
			out = (
				subprocess.check_output(shlex.split(f"avahi-resolve -a {IP}"))
				.decode()
				.split("\t")[1]
				.strip()
				.split(".")[0]
			)
			if out is f"RaspberryPiFollower{i}":
				return
			else:
				print(
					f'{con_colors.WARNING}Found an existing RaspberryPi "RaspberryPiFollower{i}" on the network{con_colors.ENDC}'
				)
		print(
			f"{con_colors.FAIL}Too many Follower RaspberryPis on the network. Can't continue{con_colors.ENDC}"
		)
		raise SystemExit()


os.system("clear")

print(
	f"{con_colors.WARNING}Warning: this script upgrades your Raspberry Pi to the latest version using apt full-upgrade"
)
print(
	f"THIS ACTION MAY REMOVE PACKAGES, USE AT YOUR OWN RISK{con_colors.ENDC}\nPress Ctrl+C to close"
)

input(f"{con_colors.BOLD}Press Enter to continue{con_colors.ENDC}")

print(
	f"""
{con_colors.BOLD}Is this Raspberry Pi a leader or follower?{con_colors.ENDC}
{con_colors.OKBLUE} a) {con_colors.ENDC}Leader
{con_colors.OKBLUE} b) {con_colors.ENDC}Follower
{con_colors.GRAY} c) Skip mDNS setup{con_colors.ENDC} 

{con_colors.BOLD}Option (a/b/c):{con_colors.ENDC} """,
	end="",
)
while True:
	choice = str(input()).lower()
	if choice == "a":
		handle_hostname(1)
	elif choice == "b":
		handle_hostname(2)
	elif choice == "c":
		print(
			f"{con_colors.WARNING}Skipping mDNS setup. This may prevent other Pis from finding this Pi on the network{con_colors.ENDC}"
		)
		break
	else:
		print(f"{con_colors.WARNING}Enter a, b, or c{con_colors.ENDC}")
		continue
	print(f"{con_colors.OKCYAN}Finished mDNS setup{con_colors.ENDC}")
	break


print(
	f"""
{con_colors.BOLD}A hostname is required for us to display the control information and camera feed on a website.
By default we use DuckDNS as it's a free and easy service. You may change this if you are technically savvy.

A hostname may look like peltier.duckdns.org. You may register one at DuckDNS.org.
A token will be of the form xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx, and you may find it by logging in to
DuckDNS.org from a web browser and looking for the 'token:' field

{con_colors.UNDERLINE}{con_colors.WARNING}Entering these values constitutes the acceptance of LetsEncrypt TOS (https://letsencrypt.org/repository/){con_colors.ENDC}  
"""
)

user_hostname = ""
while not user_hostname.endswith(".duckdns.org"):
	user_hostname = input(
		f"{con_colors.BOLD}Enter the hostname (xxxxx.duckdns.org):{con_colors.ENDC} "
	)
user_duckdns_token = ""
while len(user_duckdns_token) != 36:
	user_duckdns_token = input(
		f"{con_colors.BOLD}Enter the token (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx):{con_colors.ENDC} "
	)
user_email = ""
while "@" not in user_email:
	user_email = input(
		f"{con_colors.BOLD}Enter the email SSL certificates will be issued for (xxxx@xxxx.com):{con_colors.ENDC} "
	)

with open(f"{os.getcwd()}/.env", "w") as file:
	file.writelines(
		[
			f"USER_HOSTNAME={user_hostname}\n",
			f"USER_EMAIL={user_email}\n",
			f"USER_DUCKDNS_TOKEN={user_duckdns_token}\n",
		]
	)
	print(
		f"{con_colors.OKCYAN}Saved your configuration to the .env file, for use with Docker{con_colors.ENDC}"
	)

run_shell(
	"apt update",
	f"{con_colors.OKCYAN}Updated package lists",
	f"{con_colors.FAIL}Can't update package lists. {failure_warning}",
	True,
)
run_shell(
	"apt full-upgrade -y",
	f"{con_colors.OKCYAN}Upgraded system",
	f"{con_colors.FAIL}Couldn't upgrade the system. The setup will attempt to continue, but results can no longer be guaranteed",
)
run_shell(
	"apt install -y avahi-utils avahi-daemon git python3 python3-pip cron",
	f"{con_colors.OKCYAN}Installed prerequisite programs",
	f"{con_colors.FAIL}Could not install prerequisite programs. {failure_warning}",
	True,
)
if (
	run_shell(
		"command -v docker",
		f"{con_colors.OKCYAN}Docker is already installed, skipping",
		f"{con_colors.OKCYAN}Installing Docker",
		True,
		True,
	)
	!= 0
):
	print(
		f"{con_colors.GRAY}We're installing Docker. This may take a while, and it may look like there's no progress at all. Please sit tight.{con_colors.ENDC}"
	)
	run_shell(
		'bash -c "$(curl -fsSL https://get.docker.com)"',
		f"{con_colors.OKCYAN}Successfully installed the Docker runtime",
		f"{con_colors.FAIL}Unable to install Docker. {failure_warning}",
		True,
	)
pip_install("docker-compose")
run_shell(
	f"mv --backup=t {os.getcwd()}/docker-compose.yml {os.getcwd()}/docker-compose-old.yml",
	f"{con_colors.WARNING}Renamed your old docker-compose.yml to docker-compose-old.yml",
)
run_shell(
	f'bash -c "curl "https://raw.githubusercontent.com/y-almannaee/tecberry/main/docker-compose-default.yml" > {os.getcwd()}/docker-compose.yml"',
	f"{con_colors.OKCYAN}Downloaded latest docker-compose.yml",
	f"{con_colors.FAIL}Unable to get latest docker-compose.yml. {failure_warning}",
	True,
)
for path in [
	Path("./app_data/redis/data"),
	Path("./app_data/public/docs"),
	Path("./app_data/public/google"),
	Path("./app_data/authenticators"),
]:
	path.resolve().mkdir(mode=774, parents=True, exist_ok=True)
run_shell(
	f'bash -c "curl "https://raw.githubusercontent.com/y-almannaee/tecberry/main/docker-src/redistimeseries.so" -o {os.getcwd()}/app_data/redis/redistimeseries.so',
	f"{con_colors.OKCYAN}Downloaded redis time series module",
	f"{con_colors.FAIL}Unable to download redis time series module. {failure_warning}",
	True,
)
run_shell(
	f'bash -c "curl "https://raw.githubusercontent.com/y-almannaee/tecberry/main/docker-src/google_authentication.py" -o {os.getcwd()}/app_data/authenticators/google_authentication.py',
	f"{con_colors.OKCYAN}Downloaded default authenticator",
	f"{con_colors.FAIL}Unable to download default authenticator. {failure_warning}",
	False,
)
run_shell(
	f'bash -c "chown -R pi:pi {os.getcwd()}/app_data {os.getcwd()}/docker-compose.yml {os.getcwd()}/.env"',
	f"{con_colors.OKCYAN}Created ./app_data and transferred ownership of all requisite files to the pi user",
	f"{con_colors.FAIL}Unable to create ./app_data folder or change ownership of files. {failure_warning}",
	True,
)
print(
	f"{con_colors.GRAY}We're pulling the latest Docker images. This may take a while, and it may look like there's no progress at all. Please sit tight.{con_colors.ENDC}"
)
run_shell(
	"/usr/local/bin/docker-compose pull",
	f"{con_colors.OKCYAN}Pulled latest Docker images",
	f"{con_colors.FAIL}Unable to pull latest Docker images. Ensure that the docker-compose module was downloaded by Python and that it is in the /usr/local/bin folder. {failure_warning}",
	True,
	stdout_to=subprocess.STDOUT,
)
if run_shell(
	f"/usr/bin/docker run --rm -e DUCKDNS_TOKEN={user_duckdns_token} -v {os.getcwd()}/app_data:/var/lib goacme/lego --accept-tos --path /var/lib/ --email {user_email} --dns duckdns --domains {user_hostname} --domains *.{user_hostname} run",
	f"{con_colors.OKCYAN}Successfully ran the LetsEncrypt container, generated certificates were placed in the ./app_data folder",
	f"{con_colors.WARNING}Unable to successfully run the LetsEncrypt container",
	False,
) != 0 and not os.path.exists(f"{os.getcwd()}/app_data/certificates"):
	print(
		f"{con_colors.FAIL}Failure obtaining SSL certificates. Your web connections to this RaspberryPi will not be encrypted securely. Ensure that Docker is installed successfully. {failure_warning}{con_colors.ENDC}"
	)
else:
	print(
		f"{con_colors.OKCYAN}Certificates exist in ./app_data. If they are outdated they will be renewed when you run the docker-compose containers.{con_colors.ENDC}"
	)

with open("/etc/cron.d/lego-renew", "w") as file:
	file.writelines(
		["echo '44 4 * * * root /usr/local/bin/docker-compose up letsencryptgo"]
	)
	print(
		f"{con_colors.OKCYAN}Added recurring job to renew SSL certificates for your hostname{con_colors.ENDC}"
	)

print(
	f"\n{con_colors.OKGREEN}Successfully finished setup. Run the containers using {con_colors.ENDC}{con_colors.BOLD}sudo docker-compose pull && sudo docker-compose up -d{con_colors.ENDC}"
)
print(
	f"{con_colors.WARNING}Report any issues to {con_colors.ENDC}{con_colors.BOLD}https://github.com/y-almannaee/tecberry/issues{con_colors.ENDC}"
)
if not (len(sys.argv) == 2 and sys.argv[1] == "--no-rm"):
	print(
		f"{con_colors.GRAY}This script automatically removes itself to prevent running outdated commands. To prevent this behaviour pass --no-rm to the invoking interpreter."
	)
	os.remove(sys.argv[0])
