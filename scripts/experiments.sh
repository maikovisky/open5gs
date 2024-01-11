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


start_slice1() {
    experiment="$1"
    annotation "$experiment"
    for num in 1 5 10 15 20 25  
    do
       echo "UEs: $num"
       annotation "Numero de UEs: $num"
       kubectl scale --replicas=4 deployment open5gs-ue01
       sleep 495s 
    done 

    kubectl scale --replicas=0 deployment open5gs-ue01
}


start() {
    experiment="$1"
    upf4=$(kubectl get pod | grep open5gs-upf-4 | awk '{print $1}')
    kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth-
    annotation "$experiment"
    sleep 120s

    for num in 1 5 10 15 20 25  
    do
       echo "UEs: $num"
       annotation "Numero de UEs: $num"
       kubectl scale --replicas=4 deployment open5gs-ue01
       kubectl scale --replicas=$num deployment open5gs-ue02
       kubectl scale --replicas=$num deployment open5gs-ue03
       kubectl scale --replicas=$num deployment open5gs-ue04
       kubectl scale --replicas=$num deployment open5gs-ue05
       sleep 495s 
    done 

    for num in 100 75 50 25 10 5 1
    do
        echo "Bandwith: $num"
        annotation "Change bandwith: $num M"
        kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth=${num}M --overwrite
        sleep 495s 
    done 

    kubectl scale --replicas=0 deployment open5gs-ue01
    kubectl scale --replicas=0 deployment open5gs-ue02
    kubectl scale --replicas=0 deployment open5gs-ue03
    kubectl scale --replicas=0 deployment open5gs-ue04
    kubectl scale --replicas=0 deployment open5gs-ue05

    annotation "Fim do experimento"
}


#changeLimits 1 "0" "0"
#changeLimits 2 "0" "0"
#changeLimits 3 "0" "0"
#changeLimits 4 "0" "0"

start "Experimento 01 - Slice,CPU,MEM: [UPF1,nd,nd] [UPF2,nd,nd] [UPF3,nd,nd] [UPF4,nd,nd]"

changeLimits 1 "1200m" "250Mi"
changeLimits 2 "1200m" "250Mi"
changeLimits 3 "1200m" "250Mi"
#changeLimits 4 "0" "0"

start "Experimento 02 - Slice,CPU,MEM: [UPF1,1200,250] [UPF2,1200,250] [UPF3,1200,250] [UPF4,nd,nd]"

#changeLimits 1 "1200m" "250Mi"
changeLimits 2 "0" "0"
#changeLimits 3 "1200m" "250Mi"
changeLimits 4 "1200m" "250Mi"

start "Experimento 03 - Slice,CPU,MEM: [UPF1,1200,250] [UPF2,nd,nd] [UPF3,1200,250] [UPF4,1200,1200]"


changeLimits 3 "0" "0"
changeLimits 4 "0" "0"
#changeLimits 1 "1200m" "250Mi"
changeLimits 2 "1200m" "250Mi"

start "Experimento 03 - Slice,CPU,MEM: [UPF1,1200,250] [UPF2,1200,250] [UPF3,nd,nd] [UPF4,1200,1200]"
