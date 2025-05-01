#!/bin/bash

val=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

for s in $(serial)
do
    case $val in
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

