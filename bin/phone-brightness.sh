#!/bin/bash

val=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    echo $s
    adb -s $s shell     settings put system screen_brightness $val &
done

