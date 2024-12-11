#/!bin/bash

first=1
last=6

while true;
do
    for i in $(seq ${first} ${last})
    do
        ps -ef |grep scrcpy |grep --silen 300$i
        if [ $? -eq 0 ]; then
            echo scrcpy is running
        else
            echo restarting scrcpy on port 300$i logfile /tmp/sc-300$i.log
            ./start-zapper.sh $i >/tmp/sc-300$i.log  2>&1 &
        fi
    done
    sleep 10
done
