#!/bin/sh

annotation() {
  varText=$1
  t=$(date +%s%N | cut -b1-13)
  curl --location 'http://admin:admin@10.108.100.140:3000/api/annotations'  --header 'Accept: application/json'  --header 'Content-Type: application/json' --data "{ \"dashboardUID\": \"9ZtOvTcVz\", \"panelId\": 54, \"time\":$t, \"text\": \"$varText\", \"tags\": [\"open5gs\"]}"

}

changeLimits() {
  UPF=$1
  CPU=$2
  MEM=$3

  c='{"spec":{"template":{"spec":{"containers":[{"name":"upf'$UPF'", "resources":{"requests":{"cpu":"'$CPU'", "memory": "'$MEM'"}, "limits":{"cpu":"'$CPU'", "memory": "'$MEM'"}}}]}}}}'

  kubectl scale --replicas=0 deployment open5gs-upf-$UPF
  kubectl scale --replicas=0 deployment open5gs-ueransim0$UPF
  kubectl patch deployment open5gs-upf-$UPF -p "$c"
  kubectl get pods  open5gs-upf-$UPF
  kubectl scale --replicas=1 deployment open5gs-upf-$UPF
  while true
  do
    a=$(kubectl get pods | grep Running | grep upf- | wc -l)
    if [ $a -eq 4 ]; then
       break 
    fi
    sleep 5s
  done
  kubectl scale --replicas=1 deployment open5gs-ueransim0$UPF
}


start() {
    experiment="$1"
    #upf4=$(kubectl get pod | grep open5gs-upf-4 | awk '{print $1}')
    #kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth-
    annotation "$experiment"
    sleep 30s

    kubectl scale --replicas=4 deployment open5gs-ue01
    for num in 1 5 10 15 20 25 
    do
       echo "Fase: $num"
       annotation "Fase: $num"
       kubectl scale --replicas=$num deployment open5gs-ue02
       #kubectl scale --replicas=$num deployment open5gs-ue03
       #kubectl scale --replicas=$num deployment open5gs-ue04
       sleep 300s 
    done 

    sleep 60s 
    kubectl scale --replicas=0 deployment open5gs-ue01
    kubectl scale --replicas=0 deployment open5gs-ue02
    annotation "Fim do experimento 02"
}

start "Experimento 02 - Slice,CPU,MEM: [UPF1,nd,nd] [UPF2,nd,nd] [UPF3,nd,nd] [UPF4,nd,nd]"

