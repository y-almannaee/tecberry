import requests, socket, sys, time, subprocess, re, os
from subprocess import PIPE

duckdns_hostname = os.environ.get("USER_DUCKDNS_HOSTNAME", "")
duckdns_token = os.environ.get("USER_DUCKDNS_TOKEN", "")

if not duckdns_hostname or not duckdns_token:
	raise SystemExit

try:
	resolve_dns = socket.getaddrinfo(duckdns_hostname, 0, 0, 0)
except socket.gaierror:
	raise SystemExit
current_ips = set()

for i in resolve_dns:
	current_ips.add(i[4][0])

with subprocess.Popen(
	["curl", "-4sL", "https://cloudflare.com/cdn-cgi/trace"], stdout=PIPE
) as proc:
	raw_v4 = proc.stdout.read()

with subprocess.Popen(
	["curl", "-6sL", "https://cloudflare.com/cdn-cgi/trace"], stdout=PIPE
) as proc:
	raw_v6 = proc.stdout.read()

time_format = "[%H:%M:%S %Y/%m/%d] "
if (b"cloudflare.com" in raw_v4) and (b"cloudflare.com" in raw_v6):
	ipv4 = re.search("\nip=(.*)\n", raw_v4.decode()).group(1)
	ipv6 = re.search("\nip=(.*)\n", raw_v6.decode()).group(1)

	if (ipv4 not in current_ips) or (ipv6 not in current_ips):
		update_url = f"https://www.duckdns.org/update?domains={duckdns_hostname}&token={duckdns_token}&verbose=true&ip={ipv4}&ipv6={ipv6}"
		update = requests.get(update_url)
		print(
			time.strftime(time_format, time.localtime()),
			"DuckDNS IP update result",
			update.text.replace("\n", " "),
			"\n",
		)
else:
	print(
		time.strftime(time_format, time.localtime()),
		"Failed to reach cloudflare.com/cdn-cgi/trace\n",
	)
