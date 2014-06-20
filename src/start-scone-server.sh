#!/bin/bash

PIDFILE=scone-server.pid

trap "{ ./stop-server; exit 0; }" SIGINT SIGTERM SIGKILL

cd /opt/scone/scone-server-1.0/
if [ -f $PIDFILE ]; then
    ./stop-server
fi

./start-server 5000 -noxml

while true; do
    sleep 1
done
