#!/bin/bash

source poke-lib.sh

fight()
{
    # while sleep 0.01
    # while ! check_color 285 182 5 5 5 5 1
    # while ! check_color 176 624 253 253 243 10 1
    while sleep 0.1
    do
        click 245 890
        click 145 890

        click 164 821 1

        for (( x = 50; x < 450 ; x += 100 ))
        do
            # check_color 285 182 5 5 5 5 || return
            for (( y = 370; y < 777; y += 130 ))
            do
                # sleep 0.15
                click $x $y
            done
            click 260 821 1
            sleep 0.15
            click 230 871 1

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
