#!/bin/bash

# start battle : color:264,865,112,175,92
# great league : color:179,499,255,255,255
# let battle : color:178,631,160,219,149


# rematch : color:144,650,163,220,148
# use this party : color:194,912,163,220,148
# until black screen : olor:317,844,60,75,122


echo $2

if [ $# -ne 2 ]; then
    echo give pipe args
fi

export PORT="$1"

export PORTS=($1 $2)

source poke-lib.sh

traded=1


while true
do

    for PORT in ${PORTS[*]}
    do
        timeout=20
        echo "Waiting for rematch $PORT"
        while ! check_color 144 650 163 220 148 10
        do
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No rematch $PORT"
                exit 1
            fi
            sleep 1
        done
        sleep 0.5
        click 144 617 400
    done

    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for use this party $PORT"
        while ! check_color 194 912 163 220 148 10
        do
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "Use this party $PORT"
                exit 1
            fi
            sleep 1
        done
        sleep 0.5
        click 194 912
    done

    for (( x = 166  ; x < 700 ; x += 120 )) do
        for PORT in ${PORTS[*]}
        do
            click $x 844
        done
        sleep 0.5
        check_color 100 300 10 10 10 10 && break
        check_color 144 650 163 220 148 10 && break
    done

done
