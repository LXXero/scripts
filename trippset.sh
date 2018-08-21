#!/bin/bash

statefile=/home/xero/misc/scripts/.trippset

if [ $1 ]; then
  action=$1
else
  while [ $((`stat -c %Y $statefile` + 20)) -gt `date +%s` ]; do
   sleep 1 
  done

  state=`snmpget -v2c -ctripplite xtripplite.x TRIPPLITE::tripplite.100.1.10.2.1.2.2 -Oqv`
  echo "Current state is $state. Statefile was `cat $statefile`"
  [ "$state" == "2" ] && action="off"
fi

if [ "$action" == "off" ]; then
  snmpset -v2c -ctripplite -Oqv xtripplite.x TRIPPLITE::tripplite.100.1.10.2.1.4.2 integer 1 > $statefile
  echo "Turning off..."
else
  snmpset -v2c -ctripplite -Oqv xtripplite.x TRIPPLITE::tripplite.100.1.10.2.1.4.2 integer 2 > $statefile
  echo "Turning on..."
fi
