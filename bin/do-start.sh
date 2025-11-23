#/!bin/bash
#!/usr/bin/env bash
#!/usr/bin/env bash
#!/usr/bin/env bash

killall python

app="$1"
shift

trap ctrl_c INT
trap ctrl_c TERM

function ctrl_c() {
    echo "INT signal"
    # Kill all children
    for p in "${pids[@]}"
    do
        echo Killing $p
        kill $p
    done
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
    	${app} -p $port $* &
    	pid[$port]=$!
    fi
}

# echo $app | grep "\.py" ||  app="${app}.py"

[ -z "$first" ] || first=1
last=6
# killall python

pids=()
echo Check app status
for i in $(seq ${first} ${last})
do
	# echo restarting $app on port 300$i logfile /tmp/app-300$i.log
	# start_app 300$i $*	
	echo ./${app} -p 300$i $*
	${app} -p 300$i $* &
    pids+=($!)
done

while sleep 100; do sleep 1; done
