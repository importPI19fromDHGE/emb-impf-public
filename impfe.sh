#!/bin/bash
### BEGIN INIT INFO
# Default-Start: 1 2 3 4 5
# Default-Stop: 0 6
### END INIT INFO
. /lib/lsb/init-functions

start(){
bash -c "cd /home/pi/emb-impf && ./barcodescanner.py"
}

stop(){
    bash -c "killall python3"
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	*)
	   	exit 1
esac

exit 0
