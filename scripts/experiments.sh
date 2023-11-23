#!/bin/sh

MONGOURL="localhost:27017"

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
  while a=$(kubectl get pods | grep Running | grep upf- | wc -l)
  do
    if [ $a -le 4 ]
    then
        continue
    fi
  done
  kubectl scale --replicas=1 deployment open5gs-ueransim0$UPF
}

start() {
    experiment=$1
    upf4=$(kubectl get pod | grep open5gs-upf-4 | awk '{print $1}')
    kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth-
    annotation $experiment
    sleep 30s

    for num in {1,5,10,15,20,25,30}
    do
        annotation "Numero de UEs: $num"
        echo "UEs: $num"
        kubectl scale --replicas=1 deployment open5gs-ue01
        kubectl scale --replicas=$num deployment open5gs-ue02
        kubectl scale --replicas=$num deployment open5gs-ue03
        kubectl scale --replicas=$num deployment open5gs-ue04
        sleep 495s 
    done 

    for num in {100,75,50,25,10,5,1}
    do
        annotation "Change bandwith: $num M"
        echo "Bandwith: $num"
        kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth=${num}M --overwrite
        sleep 495s 
    done 

    kubectl scale --replicas=0 deployment open5gs-ue01
    kubectl scale --replicas=0 deployment open5gs-ue02
    kubectl scale --replicas=0 deployment open5gs-ue03
    kubectl scale --replicas=0 deployment open5gs-ue04

    annotation "Fim do experimento"
}

start "Experimento 04 - Slice,CPU,MEM: [UPF1,nd,nd] [UPF2,nd,nd] [UPF3,nd,nd] [UPF4,nd,nd] "

changeLimits 1 "1250m" "250Mi"
changeLimits 2 "1200m" "250Mi"
changeLimits 3 "1200m" "250Mi"

start "Experimento 05 - Slice,CPU,MEM: [UPF1,950,250] [UPF2,925,250] [UPF3,925,250] [UPF4,nd,nd] "

changeLimits 1 "1200m" "250Mi"
changeLimits 2 "0" "0"
changeLimits 3 "1200m" "250Mi"
changeLimits 4 "1200m" "250Mi"

start "Experimento 05 - Slice,CPU,MEM: [UPF1,950,250] [UPF2,925,250] [UPF3,925,250] [UPF4,nd,nd] "


