#!/bin/sh
PYTHONEX=`which python3`
LOGFILE="/var/log/irondome-out.log"
cd /usr/src

if [ $# -eq 0 ];then
  DATAMON="/data"
else
  DATAMON="$*"
fi
#disown
$PYTHONEX -u irondome.py $DATAMON > $LOGFILE 2>&1 &
echo $! > /var/run/irondome.pid
