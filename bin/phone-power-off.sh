#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

#echo len = "${#my_args[@]}"
#echo ${my_args[1]}
#echo ${my_args[0]}
#echo $my_args
# echo $(serial)
for s in $(serial)
do
    echo $s
    adb -s $s shell "su -c \"reboot -p\""
done

