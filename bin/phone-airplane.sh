#!/bin/bash

val=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

echo Serials  $(serial)
for s in $(serial)
do
    case $val in
        "off" | "disabled")
            echo "Disable airplane mode on $s"
            adb -s $s shell su -c 'settings put global airplane_mode_on 0' >/dev/null 2&>1
            adb -s $s shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false' &
            ;;
        *)
            echo "Enable airplane mode on $s"
            adb -s $s shell su -c 'settings put global airplane_mode_on 1' >/dev/null 2&>1
            adb -s $s shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true' &
            ;;
    esac
done

