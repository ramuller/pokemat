#!/bin/bash

# save db name
db=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    echo $s
    adb -s $s push $db /sdcard/Download
    adb -s $s shell "su -c \"killall com.incorporateapps.fakegps_route \""
    adb -s $s shell "su -c \"killall com.incorporateapps.fakegps_route \""
    adb -s $s shell "su -c \"killall com.incorporateapps.fakegps_route \""
    sleep 1
    # adb -s $s shell "su -c \"cp /sdcard/Download/$db /data/data/com.incorporateapps.fakegps_route/databases/FakeGPSRoutesInc.db \""

done

