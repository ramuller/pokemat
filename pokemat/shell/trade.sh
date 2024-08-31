#!/bin/bash

if [ $# -ne 2 ]; then
    echo give pipe args
    exit 1
fi

export PORT="$1"

export PORTS=($1 $2)

source poke-lib.sh

traded=1

while true
do

    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for select screen on $PORT"
        while ! check_color 301 946 28 135 149 16
        do
            # Check for new biggest
            if check_color 301 946 240 240 240 16 ; then
                click 301 946 250
            fi
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No trade complete $PORT"
                exit 1
            fi
        done
        
        click 494 849 250
    done

    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for trading screen on $PORT"
        while ! check_color 115 182 233 243 223 16
        do
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No trading screen on $PORT"
                exit 1
            fi
        done
    done
    sleep 3
    for PORT in ${PORTS[*]}
    do
        click 104 340 200
    done

    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for send OK on $PORT"
        while ! check_color 199 838 150 218 149 20
        do
            echo "click again"
            p=$PORT
            for PORT in ${PORTS[*]}
            do
                click 104 357 200
            done
            PORT=$p
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No send OK on $PORT"
                exit 1
            fi
        done
        sleep 1
        click 199 838 250
    done

    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for send NEXT on $PORT"
        while ! check_color 11 521 105 208 146 20
        do
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No send OK on $PORT"
                exit 1
            fi
        done
        sleep 1
        click 11 521 250
    done


    for PORT in ${PORTS[*]}
    do
        timeout=10
        echo "Waiting for trade complete on $PORT"
        while ! check_color 301 946 28 135 149 16
        do
            # Check for new biggest
            if check_color 301 946 240 240 240 16 ; then
                click 301 946 250
            fi
            timeout=$(( timeout - 1 ))
            echo "Countdown $timeout"
            if [ $timeout -le 0 ]; then
                echo "No trade complete $PORT"
                exit 1
            fi
        done
        sleep 1
        click 301 946 250
    done
    echo "Traded pokemons : $traded"
    traded=$(( traded + 1 ))
    sleep 1
    # exit 0
done
