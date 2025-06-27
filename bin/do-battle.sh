#/!bin/bash

killall python

# app="$1"
app=battle.py
shift

echo $app | grep "\.py" ||  app="${app}.py"

echo $$ >/tmp/do-battle.pid

[ -z "$first" ] || first=1
last=6
# killall python



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
    ${app} -p 300$i  -t league &
    echo $! >/tmp/$port.pid
}

while true
do
    echo Check
    for i in $(seq ${first} ${last})
    do
	    # echo restarting $app on port 300$i logfile /tmp/app-300$i.log
        port=300$i
        ps -ef |grep $app |grep --silent $port || start_app 300$i
    done
    sleep 1
    echo MYPID $$
done
          
