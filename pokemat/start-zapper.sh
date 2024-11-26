#!/bin/bash

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


EXTRA="-S --disable-screensaver"

cd ..

if false ; then
    true

elif [ "$1" == "1" ];then
    echo SN=$SN
    [ -z "$SN" ] && SN=ce091609f2237a1904
    echo SN=$SN
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=00 --window-y=0 --rest-api-port=300$1 
elif [ "$1" == "2" ];then
    [ -z $SN ] && SN=ce091719d290250304
    echo SN=$SN
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=600 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "3" ];then
    [ -z $SN ] && SN=ce091609ec79190d04
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=1200 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "4" ];then
    [ -z $SN ] && SN=ce0117119076d82a0c
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=1800 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "5" ];then
    [ -z $SN ] && SN=ce12160c4dac273705
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=2400 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "6" ];then
    [ -z $SN ] && SN=ce11160bc1ce7d1705
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=3000 --window-y=0 --rest-api-port=300$1
elif [ "$1" == "a40" ];then
    [ -z $SN ] && SN=R58M93ND7BF
    ./run x $EXTRA --window-title="$1" -s $SN -m 1024 --max-fps=8 --no-audio-playback --window-x=0 --window-y=1070 --rest-api-port=3040 
else
    echo unknow phone using port 3099 title $SN
    ./run x $EXTRA --window-title="$SN" -s $SN -m 1024 --max-fps=8 --no-audio-playback --rest-api-port=3099
fi
