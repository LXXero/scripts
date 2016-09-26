#!/bin/bash

countdown() {
  hour="${3:-0}"
  min="${2:-1}"
  sec="${1:-0}"
  desc="$4"
  
  while [ $hour -ge 0 ]; do
    while [ $min -ge 0 ]; do
      while [ $sec -ge 0 ]; do
        emin=$min
        esec=$sec
        ehour=''

        if [ $hour -gt 0 ]; then
          [ $min -lt 10 ] && emin="0$min"
          ehour="$hour:"
        fi

        [ $sec -lt 10 ] && esec="0$sec"

        echo -ne "$desc ($ehour$emin:$esec)\033[0K\r"
        echo -e "$desc ($ehour$emin:$esec)" > /home/xero/misc/documents/scene.txt
        let "sec=sec-1"
        sleep 1
      done
      sec=59
      let "min=min-1"
    done
    min=59
    let "hour=hour-1"
  done
}

while true; do
  xdotool key --delay 50 ctrl+alt+shift+1 &
  countdown 0 1 0 'Scene: Cichlid tank'

  xdotool key --delay 50 ctrl+alt+shift+3 &
  countdown 0 1 0 'Scene: Salt Tank'

  xdotool key --delay 50 ctrl+alt+shift+4 &
  countdown 0 3 0 'Scene: Dual View'
done
