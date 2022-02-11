#!/bin/sh
# `/sbin/setuser nginx` runs the given command as the user `nginx`.
# If you omit that part, the command will be run as root.
exec nginx 