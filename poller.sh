#!/bin/bash

decimalize() {
  for x in $@; do
    printf "%0.1f\n" $(echo $x / 10 | bc -l)
  done
}

while true; do
  kpv=$(decimalize $(modpoll -m ascii -a 1 -b9600 -d 7 -s 1 -p even /dev/ttyUSB0 -t 4  -0 -r 4096 -c 2 -1 2>&1|awk '/\[/ { print $NF }'))
  kmv=$(decimalize $(modpoll -m ascii -a 1 -b9600 -d 7 -s 1 -p even /dev/ttyUSB0 -t 4  -0 -r 4114 -1 2>&1|awk '/\[/ { print $NF }'))

echo `date +%FT%T` $kpv $kmv| sed 's/ /,/g'
sleep 1
done
