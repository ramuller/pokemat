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
            ;;
        *)
            echo "Enable silent mode zen 2 on $s"
            adb -s $s shell settings put global zen_mode 2
            adb -s $s shell settings put global zen_mode_config '{"allow_calls":false,"allow_messages":false,"allow_events":false,"allow_reminders":false,"allow_repeat_callers":false,"suppressed_visual_effects":0}'
            ;;
    esac
done

