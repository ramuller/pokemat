#!/bin/bash


declare -A team

team[3001]="plastic"
team[3002]="pokeeizu"
team[3003]="localhost"
team[3004]="222"
team[3005]="asdsad"
team[3006]=""


for p in $(seq 3001 3006)
do
    echo "$p ${team[$p]}"
    [ -n "${team[$p]}" ] && change_trainer.py -p $p "${team[$p]}" &
done
