#!/bin/bash

val=$1
shift

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

echo "Operation : $val"

start()
{
    echo "Starting Pokemon Go on $1"
    adb -s $1 shell monkey -p com.nianticlabs.pokemongo -c android.intent.category.LAUNCHER 1 &

}

stop()
{
    echo "Starting Pokemon Go on $1"
    adb -s $1 shell "su -c \"killall com.nianticlabs.pokemongo\"" &

}

for s in $(serial)
do
    echo $s
    case $val in
        start)
            echo "Starting Pokemon Go on $s"
            start $s
            ;;
        stop)
            echo "Stopping Pokemon Go on $s"
            stop $s
            ;;
        restart)
            echo "Restarting Pokemon Go on $s"
            stop $s
            sleep 2
            start $s
            ;;
        *)
            echo "Unknown operation: $val"
            exit 1
            ;;
    esac
done

