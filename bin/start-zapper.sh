#!/bin/bash

ZAPPER_DIR=$HOME/git/scrcpyzapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source $SCRIPT_DIR/phone-lib.sh

# Schlumpiz
# export SN=ce091609f2237a1904
# Pokeralle
# export SN=ce091719d290250304
# black 
# export SN=ce091609ec79190d04
# Gold
# export SN=ce0117119076d82a0c
# White
# export SN=ce12160c4dac273705
# Broken dev
# export SN=ce11160bc1ce7d1705
# Aphex
# export SN=R58N648E8EX


# [ -n "$EXTRA" ] || EXTRA="-S --disable-screensaver"
[ -n "$EXTRA" ] || EXTRA="--disable-screensaver"

STD_ARGS="-m 1024 --max-fps=8 --no-audio-playback --raw-key-events --no-resize"

cd $ZAPPER_DIR

if false ; then
    true

elif [ "$1" == "1" ];then
    echo SN=$SN
    [ -z "$SN" ] && SN=ce091609f2237a1904
    echo SN=$SN
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=00 --window-y=0 --rest-api-port=300$1 
elif [ "$1" == "2" ];then
    # [ -z $SN ] && SN=ce091719d290250304
    [ -z $SN ] && SN=$SN_3002
    echo SN=$SN
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=600 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "3" ];then
    [ -z $SN ] && SN=ce12160c4dac273705
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=1200 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "4" ];then
    [ -z $SN ] && SN=ce0117119076d82a0c
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=1800 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "5" ];then
    [ -z $SN ] && SN=ce091609ec79190d04
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=2400 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "6" ];then
    [ -z $SN ] && SN=ce11160bc1ce7d1705
    adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=3000 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "7" ];then
    # [ -z $SN ] && SN=ce01182118d5b02a0c
    [ -z $SN ] && SN=$SN_3007
    # adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=3000 --window-y=1030 --rest-api-port=300$1
elif [ "$1" == "8" ];then
    # [ -z $SN ] && SN=ce01182118d5b02a0c
    [ -z $SN ] && SN=$SN_3008
    # adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=120 --window-y=1030 --rest-api-port=300$1
elif [ "$1" == "9" ];then
    # [ -z $SN ] && SN=ce01182118d5b02a0c
    [ -z $SN ] && SN=$SN_3009
    # adb -s $SN shell "su -c \"echo 1040000 >/sys/power/cpufreq_max_limit\""
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=100 --window-y=1030 --rest-api-port=300$1
elif [ "$1" == "a40" ];then
    [ -z $SN ] && SN=R58M93ND7BF
    ./run x $EXTRA --window-title="$1" -s $SN $STD_ARGS --window-x=0 --window-y=1070 --rest-api-port=3040 
elif [ "$1" == "u" ];then
    echo unknow phone using port 3010 no $SN
    ./run x $EXTRA --window-title=3010 $STD_ARGS --window-x=0 --window-y=0 --rest-api-port=3010
else
    echo unknow phone using port 3099 title $SN
    ./run x $EXTRA --window-title="$SN" -s $SN $STD_ARGS --rest-api-port=3099
fi
