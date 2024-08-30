#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PIPE="$1"

source poke-lib.sh

battle()
{
    # while sleep 0.01
    # while ! check_color 285 182 5 5 5 5 1
    # while ! check_color 176 624 253 253 243 10 1
    # while ! check_color 528 840 231 244 233 15 1
    while true
    do
        for x in 132 286 403
        do
            click $x 898
            click $x 898
            check_color 528 840 231 244 233 15 1 && return 
            # sleep 0.2
        done
        
    done
}

for (( i = 0; i < 3; i++ )); do
    check_color 528 840 231 244 233 15 || exit 1
    click 528 840

    wait_color 189 399 137 218 154 10 100 || exit 1
    click 189 399

    battle
done


# wait_color_fail 317 137 70 207 181 10
# sleep 3
