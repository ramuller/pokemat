#!/bin/bash

sleep 5000
sleep 7200

./do-start.sh change-trainer.py -t nonenxisting
sleep 60
./do-start.sh change-trainer.py -t nonenxisting
sleep 60

../utils/power-off.sh

sudo systemctl hibernate
