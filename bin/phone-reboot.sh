#!/bin/bash

serial()
{
    adb devices |grep -v List | cut -f 1
}


for s in $(serial)
do
    echo $s
    adb -s $s shell "su -c \"reboot\"" &
done

