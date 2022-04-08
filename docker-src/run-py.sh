#!/bin/sh

exec python3 -m pip -r /etc/pyserver/requirements.txt && python3 /etc/pyserver/leader.py