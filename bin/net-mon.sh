#!/bin/bash

# port=$1

ONCE="no"
while getopts "o" opt; do
  case $opt in
    o)
      ONCE="yes"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

SCRIPT_DIR="$(dirname $0)"
source $SCRIPT_DIR/phone-lib.sh

disable_air()
{
    serial=$1
    echo "Disable airplane mode on $serial"
    adb -s $serial shell su -c 'settings put global airplane_mode_on 0' >/dev/null 2&>1
    adb -s $serial shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false' 
    adb -s $serial shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true'
}

enable_air()
{
    serial=$1
    echo "Enable airplane mode on $serial"
    adb -s $serial shell su -c 'settings put global airplane_mode_on 1' >/dev/null 2&>1
    adb -s $serial shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true'
    adb -s $serial shell su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false' 
}

while true
do
    for s in $(adb devices |grep device$  |grep ^ce |cut -f 1) ; do
        echo device $s
        adb -s $s shell dumpsys connectivity |grep --silent wlan0:
        if [ $? -ne 0 ]; then
            echo NetDown
            enable_air $s
            sleep 2 
            disable_air $s
            
        fi
    done
    if [ "$ONCE" = "yes" ]; then
        echo onshot mode
        exit 0
    fi
    sleep 20
done

    
