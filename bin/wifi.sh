#!/bin/bash

serial()
{
    adb devices |grep -v List | cut -f 1
}

op="$1"

for s in $(serial)
do
    case $op in
        "off" | "disabled")
            echo "Disable WiFi on $s"
            adb -s $s shell svc wifi disable
            ;;
        *)
            echo "Enable WiFi on $s"
            adb -s $s shell svc wifi enable
            ;;
    esac
done

