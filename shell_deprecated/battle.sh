#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PORT="$1"

source poke-lib.sh

claim_reward()
{
    echo claim reward
    click 123 976
    exit 0
}

scroll_up()
{
    s=$1
    y=$(( 120 + $1 ))
    button_down 50 $y
    for (( y ; y >= 120; y -= 3))
    do
        echo $y
        motion 50 $y
        sleep 0.05
    done
    sleep 1
    button_up 50 $y
}

next_battle()
{
    echo Next battle
    while ! check_color 200 950 150 215 155 20
    do
          scroll_up 15
    done
    sleep 1
    click 206 950
    sleep 1
    click 185 641
    sleep 1
    click 292 894
    sleep 5
    fight
    
}


# scroll_up 100
# exit 0
back_home
Menu
go_battle
# sleep 1
# click 162 408 1
# sleep 3
# fight

while true
do
    check_color 123 976 254 179 79 5 && claim_reward
    
    next_battle
    
done
