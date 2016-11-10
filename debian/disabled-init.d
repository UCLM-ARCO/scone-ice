#!/bin/sh
### BEGIN INIT INFO
# Provides:          scone-wrapper
# Required-Start:    $local_fs $network $remote_fs $syslog
# Required-Stop:     $local_fs $network $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Scone-server wrapper to ZeroC Ice
# Description: Provide Scone as a Ice Service
### END INIT INFO

# Author: Oscar Aceña Herrera <oscaracena@gmail.com>

DIR=/usr/bin
DAEMON=$DIR/scone-wrapper 
DAEMON_NAME=scone-wrapper

# Add any command line options for your daemon here
DAEMON_OPTS="--Ice.Config=/etc/scone-wrapper.conf"

# This next line determines what user the script runs as.
DAEMON_USER=root

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    start-stop-daemon \
	--start --background \
	--pidfile $PIDFILE --make-pidfile \
	--user $DAEMON_USER --chuid $DAEMON_USER \
	--startas $DAEMON -- $DAEMON_OPTS
}

do_stop () {
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
}

case "$1" in

    start|stop)
	do_${1}
	;;

    restart|reload|force-reload)
	do_stop
	do_start
	;;

    status)
	status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
	;;
    *)
	echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
	exit 1
	;;

esac
exit 0
