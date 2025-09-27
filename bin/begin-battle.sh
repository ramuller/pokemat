#!/bin/bash

echo Wait $1 seconds
sleep $1
echo Lets battle 7500s
do-battle.sh &
do_pid=$!
sleep 7200
echo Stop battlle
kill $do_pid
echo Killall python
killall python
sleep 60
echo Change trainer
do-start.sh change_trainer.py lkjdsa
sleep 60
echo Change trainer
do-start.sh change_trainer.py lkjdsa
sleep 60
phone-power-off.sh
sleep 60
echo Hibernate
sudo systemctl suspend
