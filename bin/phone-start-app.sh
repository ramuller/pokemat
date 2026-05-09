#!/bin/bash

app=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    echo $s
     adb -s $s shell "am start -n $app/.MainActivity"
done

