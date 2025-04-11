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
    ./${app} -p 300$i  -t league &
    echo $! >/tmp/$port.pid
}

echo $app | grep "\.py" ||  app="${app}.py"

[ -z "$first" ] || first=1
last=6
# killall python

for i in $(seq ${first} ${last})
do
	# echo restarting $app on port 300$i logfile /tmp/app-300$i.log
	./${app} -p 300$i $* &

done
