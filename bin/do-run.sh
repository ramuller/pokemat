#/!bin/bash

killall python

app="$1"
shift

trap ctrl_c INT
trap ctrl_c TERM

function ctrl_c() {
    echo "INT signal"
    # Kill all children
    for pf in $(ls /tmp/300*pid); do kill $(cat $pf);done
    killall python
    exit 0
}

start_app()
{
    port=$1
    shift
    pid_from_file=$(cat /tmp/$port.pid)
    echo "PI\"$pid_from_file\""
    if ! ls /proc/ |grep $(cat /tmp/$port.pid)
    then
    	echo ./${app} -p $port $*
    	./${app} -p $port $* &
    	echo $! >/tmp/$port.pid
    fi
}

echo $app | grep "\.py" ||  app="${app}.py"

[ -z "$first" ] && first=1
[ -z "$last" ] && last=6

while sleep 0.01
do
	echo Check app status
	for i in $(seq ${first} ${last})
	do
		# echo restarting $app on port 300$i logfile /tmp/app-300$i.log
		start_app 300$i $*	
		# echo ./${app} -p $port $* &
	done
	sleep 1
done
