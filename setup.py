#!/bin/python3

# This is an install script, run it by invoking
# curl -fsSLO https://raw.github.com/y-almannaee/peltier-controller/main/setup.py && sudo python3 setup.py
# on your Raspberry Pi!

import shlex, subprocess, sys, traceback, os, time


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


def run_shell(cmd, success_state="", error_state="", critical=False, shell=False):
    cmd = shlex.split(cmd) if not shell else cmd
    try:
        subprocess.check_call(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=shell
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
    with open("/etc/hosts", "a") as file:
        file.write(f"127.0.1.1 {hostname}")
    run_shell(f"hostnamectl set-hostname {hostname}")
    run_shell(f"systemctl restart avahi-daemon")
    time.sleep(5)


def handle_hostname(choice):
    run_shell("apt update", f"{con_colors.OKCYAN}Updated package lists")
    run_shell(
        "apt install -y avahi-utils",
        f"{con_colors.OKCYAN}Installed prerequisite programs",
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
        if out != "RaspberryPiLeader.local":
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
            if out is f"RaspberryPiFollower{i}.local":
                return
        print(
            f"{con_colors.FAIL}Too many Follower RaspberryPis on the network. Can't continue{con_colors.ENDC}"
        )
        raise SystemExit()


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
        break
    else:
        print(f"{con_colors.WARNING}Enter a, b, or c{con_colors.ENDC}")
        continue
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

user_hostname = input(
    f"{con_colors.BOLD}Enter the hostname (xxxxx.duckdns.org):{con_colors.ENDC} "
)
user_duckdns_token = input(
    f"{con_colors.BOLD}Enter the token (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx):{con_colors.ENDC} "
)
user_email = input(
    f"{con_colors.BOLD}Enter the email SSL certificates will be issued for (xxxx@xxxx.com):{con_colors.ENDC} "
)

with open(f"{os.getcwd()}/.env", "w") as file:
    file.writelines(
        [
            f"USER_HOSTNAME={user_hostname}",
            f"USER_EMAIL={user_email}",
            f"USER_DUCKDNS_TOKEN={user_duckdns_token}",
        ]
    )
    f"{con_colors.OKCYAN}Saved your configuration to the .env file, for use with Docker{con_colors.ENDC}"

failure_warning = "Make sure you are connected to the internet, there is enough space on the SD card, and that this script is running with Sudo permissions (sudo python3 ./setup.py)"

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
    f'bash -c "curl "https://raw.githubusercontent.com/y-almannaee/peltier-controller/main/docker-compose-default.yml" > {os.getcwd()}/docker-compose.yml"',
    f"{con_colors.OKCYAN}Downloaded latest docker-compose.yml",
    f"{con_colors.FAIL}Unable to get latest docker-compose.yml. {failure_warning}",
    True,
)
run_shell(
    f'bash -c "mkdir -p {os.getcwd()}/app_data; chown -R pi:pi {os.getcwd()}/app_data {os.getcwd()}/docker-compose.yml {os.getcwd()}/.env"',
    f"{con_colors.OKCYAN}Created app_data and transferred ownership of all requisite files to the {con_colors.BOLD}pi{con_colors.OKCYAN} user",
    f"{con_colors.FAIL}Unable to create app_data folder or change ownership of files. {failure_warning}",
    True,
)
run_shell(
    "/usr/local/bin/docker-compose pull",
    f"{con_colors.OKCYAN}Pulled latest Docker images",
    f"{con_colors.FAIL}Unable to pull latest Docker images. Ensure that the docker-compose module was downloaded by Python and that it is in the /usr/local/bin folder. {failure_warning}",
    True,
)
run_shell(
    f"/usr/bin/docker run -e DUCKDNS_TOKEN={user_duckdns_token} -v {os.getcwd()}/app_data:/var/lib goacme/lego --accept-tos --path /var/lib/ --email {user_email} --dns duckdns --domains {user_hostname} --domains *.{user_hostname} run",
    f"{con_colors.OKCYAN}Successfully ran the LetsEncrypt container, generated certificates were placed in the ./app_data folder",
    f"{con_colors.FAIL}Unable to run the LetsEncrypt container. Ensure that Docker was downloaded successfully. {failure_warning}",
    True,
)

with open("/etc/cron.d/lego-renew", "w") as file:
    file.writelines(
        ["echo '44 4 * * * root /usr/local/bin/docker-compose up letsencryptgo"]
    )
    print(
        f"{con_colors.OKCYAN}Added recurring job to renew SSL certificates for your hostname{con_colors.ENDC}"
    )

print(
    f"\n{con_colors.OKGREEN}Successfully finished setup. Run the containers using {con_colors.BOLD}sudo docker-compose up{con_colors.ENDC}"
)
print(
    f"{con_colors.WARNING}Report any issues to {con_colors.BOLD}https://github.com/y-almannaee/peltier-controller/issues{con_colors.ENDC}"
)
