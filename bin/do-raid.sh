#/!bin/bash

killall python

# app="$1"
app=raid.py
shift

echo $app | grep "\.py" ||  app="${app}.py"

[ -z "$first" ] || first=1
last=6
# killall python

for i in $(seq ${first} ${last})
do
	# echo restarting $app on port 300$i logfile /tmp/app-300$i.log
	./${app} -p 300$i  &
done
