#!/bin/bash
write_log()
{
  message=$1
  timestamp=$(date +"%Y-%m-%dT%H:%M:%S%z")
  echo "$timestamp $message" >> log.txt
}

main_dir="/home/pi/usbdrv/gnucash"
gnu_file="/home/pi/usbdrv/gnucash/data/v1.0/v1.0.gnucash"
gnu_file_modified_time=$(date -ur $gnu_file +%s)

cd $main_dir || exit
info_file="info.txt"
last_run_time=$(grep -Po "(?<=^last_run_time=).*" $info_file)

timestamp=$(date +"%Y-%m-%dT%H:%M:%S%z")
difference=$(($last_run_time-$gnu_file_modified_time))
if [[ $difference =~ ^[0-9]+$ ]] # contains numbers only (positive = last run greater than modified)
then
  write_log "Already ran at $last_run_time, modified: $gnu_file_modified_time"
  write_log "-----------"
  exit
else
  write_log "Difference: $difference"
  write_log "-----------"
fi

cd /home/pi/usbdrv/gnucash/python_projects || exit
git pull
cd report || exit
python main.py
cp -r /home/pi/usbdrv/gnucash/python_projects/report/output/*  /home/pi/usbdrv/gnucash/reports/

cd $main_dir || exit
current_time=$(date +%s)
echo "last_run_time=$current_time" > $info_file

timestamp=$(date +"%Y-%m-%dT%H:%M:%S%z")
write_log "Completed. Last ran: $last_run_time, modified: $gnu_file_modified_time"
write_log "-----------"
