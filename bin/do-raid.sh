#/!bin/bash

killall python

trap ctrl_c INT
trap ctrl_c TERM

function ctrl_c() {
    echo "INT signal"
    # Kill all children
    for pf in $(ls /tmp/300*pid); do kill $(cat $pf);done
    killall python
    exit 0
}

# app="$1"
app=raid.py
shift

echo $app | grep "\.py" ||  app="${app}.py"

[ -z "$first" ] || first=1
last=6
# killall python

for i in $(seq ${first} ${last})
do
	# echo start $app on port 300$i logfile /tmp/app-300$i.log
    ./${app} -p $port $* &
    echo $! >/tmp/$port.pid
done

while sleep 2
do
    echo Press CTRL-C to stop
done
