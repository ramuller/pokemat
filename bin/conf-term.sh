#!/bin/bash

count=6
[ -z "$1" ] || count=$1

split_term()
{
    if [ "$1" == "up" ] && offset=80 || offset=40 ; then
        xdotool mousemove --window $(xdotool getactivewindow) 130 10
        xdotool mousedown --window $(xdotool getactivewindow) 1
        xdotool mouseup --window $(xdotool getactivewindow) 1
        xdotool mousemove --window $(xdotool getactivewindow) 130 $offset
        xdotool mousedown --window $(xdotool getactivewindow) 1
        xdotool mouseup --window $(xdotool getactivewindow) 1
    fi
}

split_term "up"
sleep 0.1
	
for (( i = 0 ; i < $count - 1 ; i++ ))
do
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
    split_term "left"
	sleep 0.1
    
done
[ -z "$2" ] || exit 0

xdotool type "export PHONE_PORT=$(( 3001 + $i))"
xdotool key Return
xdotool mousemove --window $(xdotool getactivewindow) 130 150
xdotool mousedown --window $(xdotool getactivewindow) 1
xdotool mouseup --window $(xdotool getactivewindow) 1
for (( i = 0 ; i < $count - 1 ; i++ ))
do
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
    split_term "left"
	sleep 0.02
done
xdotool type "export PHONE_PORT=$(( 3001 + $i))"
xdotool key Return
