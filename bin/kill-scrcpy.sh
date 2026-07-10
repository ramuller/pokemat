#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    echo $s
     adb -s $s shell "su -c \"killall app_process\""
done

