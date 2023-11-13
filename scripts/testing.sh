#!/bin/bash
#numbers={1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50}
#for num in $numbers
#sleep 120s 

varText="TESTE"
function annotation {
  t=$(date +%s%N | cut -b1-13)
  curl --location 'http://admin:admin@10.108.100.140:3000/api/annotations'  --header 'Accept: application/json'  --header 'Content-Type: application/json' --data "{ \"dashboardUID\": \"9ZtOvTcVz\", \"panelId\": 54, \"time\":$t, \"text\": \"$varText\", \"tags\": [\"open5gs\"]}"

}

upf2=$(kubectl get pod | grep open5gs-upf-2 | awk '{print $1}')
upf4=$(kubectl get pod | grep open5gs-upf-4 | awk '{print $1}')

# Removendo restrições de banda
kubectl annotate pod $upf4 kubernetes.io/egress-bandwidth-

varText="Inicio do experimento 04 - Slice,CPU,MEM: [UPF1,900,250] [UPF2,900,250] [UPF3,900,250] [UPF4,900,250] "
annotation
sleep 5s

#for num in {1,2,3,4,5,6,7,8,9,10,15,20,25,30}
for num in {1,5,10,15,20,25,30}
do
    varText="Numero de UEs: $num"
    annotation
    echo "UEs: $num"
    kubectl scale --replicas=1 deployment open5gs-ue01
    kubectl scale --replicas=$num deployment open5gs-ue02
    kubectl scale --replicas=$num deployment open5gs-ue03
    kubectl scale --replicas=$num deployment open5gs-ue04
    #kubectl scale --replicas=$num deployment open5gs-ue05
    #kubectl scale --replicas=$num deployment open5gs-ue06
    #kubectl scale --replicas=$num deployment open5gs-ue07
    #kubectl scale --replicas=$num deployment open5gs-ue08
    sleep 495s 
done 

for num in {100,75,50,25,10,5,1}
do
    varText="Change bandwith: $num M"
    annotation
    echo "Bandwith: $num"
    kubectl annotate pod $upf2 kubernetes.io/egress-bandwidth=${num}M --overwrite
    sleep 495s 
done 


kubectl scale --replicas=0 deployment open5gs-ue01
kubectl scale --replicas=0 deployment open5gs-ue02
kubectl scale --replicas=0 deployment open5gs-ue03
kubectl scale --replicas=0 deployment open5gs-ue04
#kubectl scale --replicas=0 deployment open5gs-ue05
#kubectl scale --replicas=0 deployment open5gs-ue06
#kubectl scale --replicas=0 deployment open5gs-ue07
#kubectl scale --replicas=0 deployment open5gs-ue08
varText="Fim do experimento"
annotation
