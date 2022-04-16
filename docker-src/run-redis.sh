#!/bin/sh

exec /usr/bin/redis-server --loadmodule /bin/redistimeseries.so --save 60 1 --loglevel notice