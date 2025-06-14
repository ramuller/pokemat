#!/bin/bash

if ! echo $PATH |grep -silent pokemat
then
    # pd="$(dirname "$(cd "$(dirname "$0")" && pwd)")"
    pd="/space/home/ralf/git/pokemat"
    echo Add pokemat patch $pd
    export PATH="$PATH:$pd/bin:$pd/pokemat"
    export PYTHONPATH="$PYTHONPATH:$pd/lib"
fi
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
sleep 0.3
	
for (( i = 0 ; i < $count - 1 ; i++ ))
do
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
    split_term "left"
	sleep 0.3
    
done
[ -z "$2" ] || return

xdotool type "export PHONE_PORT=$(( 3001 + $i))"
xdotool key Return
xdotool mousemove --window $(xdotool getactivewindow) 130 150
xdotool mousedown --window $(xdotool getactivewindow) 1
xdotool mouseup --window $(xdotool getactivewindow) 1
# for (( i = 0 ; i < $count - 1 ; i++ ))
for (( i = 0 ; i < 3 - 1 ; i++ ))
do
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
	xdotool type "export PHONE_PORT=$(( 3001 + $i))"
	xdotool key Return
    split_term "left"
	sleep 0.03
done
xdotool type "export PHONE_PORT=$(( 3001 + $i))"
xdotool key Return
