#!/bin/bash


hasSlice() {
  for SLICE in $slices; do
    if [ "$SLICE" = "$1" ]; then
      return 0
    fi
  done
  return 1
}

imsi=$(nr-cli --dump)
slice=$(nr-cli $imsi -e ps-list | awk '/apn: / {print $2}' | awk 'END{print}')

mqtt="-t $slice"

echo $mqtt
#if  hasSlice "slice01";then
#  echo "OPA"
#fi

while true
do
   echo "Waiting experience..." 
   mosquitto_sub -h open5gs-mqtt $mqtt -C 1 > mqtt.json
   status=$(jq -r .status mqtt.json)
   cmd=$(jq -r .cmd mqtt.json)

   if [ $status != "config" ]; then
      echo "No config $status"
      continue
   fi

   echo "Waiting for approval.."
   mosquitto_pub -h open5gs-mqtt -t $slice/ue/$imsi -m "{/"imsi/": /"$imsi/", /"slice/": /"$slice/"}"
   mosquitto_sub -h open5gs-mqtt -t $slice/ue/$imsi -C 1 > mqtt.json
   status=$(jq -r .status mqtt.json)
   if [ "$status" = "nok" ]; then
      echo "Not approve"
      continue
   fi

   echo "Approve!! Waiting for the experiment to start. "
   mosquitto_sub -h open5gs-mqtt -t "start" -C 1
   echo "start iperf $cmd"
   sleep 5s
   #mosquitto_sub -h open5gs-mqtt $mqtt -C 1 > mqtt.json

   echo "Finish"
   mosquitto_pub -h open5gs-mqtt -t "finish" -m "finish"
 done