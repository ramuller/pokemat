#!/bin/bash


phone=$1

while true
do
    cd ..
    ./start.sh $phone &
    pid=$!
    echo scrcpy pid $pid
    cd -
    sleep 10
    ./battle.py --type trainer$(( 1 + $1 % 3)) --league ultra --port 300$phone
    killall scrcpy
    sleep 10
done

# Start 266
