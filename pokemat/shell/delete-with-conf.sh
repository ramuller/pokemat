#!/bin/bash

if [ $# -ne 1 ]; then
    echo give pipe arg
    exit 1
fi

export PIPE="$1"

source poke-lib.sh


click 82 322
sleep 1.5
click 401 913
sleep 1.5
click 347 820
sleep 1
click 176 563
sleep 1
click 255 535

