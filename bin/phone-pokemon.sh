#!/bin/bash

val=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

echo "Operation : $val"

for s in $(serial)
do
    echo $s
    if [[ "$val" = "start" ]] ; then
        adb -s $s shell monkey -p com.nianticlabs.pokemongo -c android.intent.category.LAUNCHER 1
    else
        adb -s $s shell "su -c \"killall com.nianticlabs.pokemongo\""
    fi
done

