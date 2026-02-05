#!/bin/sh

# Install
# 
# Checks
# Max
# cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
# Current
# cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# lowpower core
FPL=832000
#  performance core
FPC=1170000

echo "CPUFreq start" >/data_mirror/cpufreq.log


# wait until Android boot is complete
while [ "$(getprop sys.boot_completed)" != "1" ]; do
    echo "CPUFreq wait for boot ready" >>/data_mirror/cpufreq.log

    sleep 2
done
echo "CPUFreq sleep bit more" >>/data_mirror/cpufreq.log

# optional extra delay (cpufreq HAL often kicks in late)
sleep 5

echo "CPUFreq adjusted"
echo "CPUFreq adjusted" >>/data_mirror/cpufreq.log

echo $FPL >/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
echo $FPC >/sys/devices/system/cpu/cpu7/cpufreq/scaling_max_freq    
