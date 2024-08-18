#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PIPE="$1"

source poke-lib.sh

fight()
{
    # while sleep 0.01
    # while ! check_color 285 182 5 5 5 5 1
    while ! check_color 176 624 253 253 243 10 1
    do

        for (( x = 226; x < 240 ; x += 25 ))
        do
            # check_color 285 182 5 5 5 5 || return
            for (( y = 530; y < 700; y += 30 ))
            do
                click $x $y
            done
        done
        
    done
}

# back_home
# Menu
# go_battle

fight

exit 0


click 350 742
sleep 3
click 350 742
sleep 3
wait_color_fail 317 137 70 207 181 10
sleep 3
