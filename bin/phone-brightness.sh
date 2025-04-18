#!/bin/bash

serial()
{
    adb devices |grep -v List | cut -f 1
}


for s in $(serial)
do
    echo $s

    adb -s $s shell     settings put system screen_brightness $1 &
done

