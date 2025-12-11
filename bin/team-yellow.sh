#!/bin/bash


declare -A team

team[3001]="higimmi222"
team[3002]="pokeralle"
team[3003]="plastic"
team[3004]="Yellowthatsit"
team[3005]="blond"
team[3006]="Higimmi1234"


for p in $(seq 3001 3006)
do
    echo "$p ${team[$p]}"
    [ -n "${team[$p]}" ] && change_trainer.py -p $p "${team[$p]}" &
done
