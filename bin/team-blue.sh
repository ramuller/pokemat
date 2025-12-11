#!/bin/bash


declare -A team

team[3001]="helmut"
team[3002]="eizu123"
team[3003]="blue"
team[3004]=""
team[3005]=""
team[3006]=""


for p in $(seq 3001 3006)
do
    echo "$p ${team[$p]}"
    [ -n "${team[$p]}" ] && change_trainer.py -p $p "${team[$p]}" &
done
