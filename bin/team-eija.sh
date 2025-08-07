#!/bin/bash


declare -A team

team[3001]="blond"
team[3002]="pokeeizu"
team[3003]="plastic"
team[3004]="222"
team[3005]="local"
team[3006]=""


for p in $(seq 3001 3006)
do
    echo "$p ${team[$p]}"
    [ -n "${team[$p]}" ] && change_trainer.py -p $p "${team[$p]}" &
done
