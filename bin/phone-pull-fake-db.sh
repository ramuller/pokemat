#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    echo $s
    adb -s $s shell "su -c \"ls -l /data/data/com.incorporateapps.fakegps_route/databases/FakeGPSRoutesInc.db\""
    adb -s $s shell "su -c \"cp /data/data/com.incorporateapps.fakegps_route/databases/FakeGPSRoutesInc.db /sdcard/Download \""
    adb -s $s pull "/sdcard/Download/FakeGPSRoutesInc.db" FakeGPSRoutesInc.db-$s
done

