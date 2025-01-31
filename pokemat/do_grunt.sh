#!/bin/bash


PORT="$1"

./heal.py -p $PORT || exit 1

while sleep 1; do
    ./grunt.py -p $PORT
    ./heal.py -p $PORT
    # ./heal.py -p $PORT
    # ./heal.py -p $PORT || exit 1
done
