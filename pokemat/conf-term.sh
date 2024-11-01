#!/bin/bash

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

split_term "left"
split_term "left"

xdotool mousemove --window $(xdotool getactivewindow) 130 150
xdotool mousedown --window $(xdotool getactivewindow) 1
xdotool mouseup --window $(xdotool getactivewindow) 1

split_term "left"
split_term "left"

