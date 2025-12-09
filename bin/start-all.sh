#/!bin/bash

first="$1"
last="$2"

[ -n "$1" ] || first=1
[ -n "$2" ] || last=7

thisdir="$(dirname $0)"

net_mon()
{
    net_port=$1
    state="$(read-text.py -p $net_port 310 140 280 70)"
    echo "$state" |grep 'No Internet'
    if [ $? -eq 0 ]; then
        echo "Restore internet"
        phone-airplane.sh on $net_port
        sleep 3
        phone-airplane.sh off $net_port
    fi
}

while true;
do
    for i in $(seq ${first} ${last})
    do
        port=300$i
        ps -ef |grep scrcpy |grep --silent 300$i
        if [ $? -eq 0 ]; then
            echo scrcpy is running
        else
            echo restarting scrcpy on port 300$i logfile /tmp/sc-300$i.log
            $thisdir/start-zapper.sh $i >/tmp/sc-300$i.log  2>&1 &
        fi
        # net_mon $port
    done
    sleep 10
done
