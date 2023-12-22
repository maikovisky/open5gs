#!/bin/bash
#numbers={1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50}
#for num in $numbers
sleep 120s 

for num in {1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50}
do
    echo $num
    kubectl scale --replicas=1 deployment open5gs-ue01
    kubectl scale --replicas=$num deployment open5gs-ue02
    kubectl scale --replicas=$num deployment open5gs-ue03
    kubectl scale --replicas=$num deployment open5gs-ue04
    #kubectl scale --replicas=$num deployment open5gs-ue05
    #kubectl scale --replicas=$num deployment open5gs-ue06
    #kubectl scale --replicas=$num deployment open5gs-ue07
    #kubectl scale --replicas=$num deployment open5gs-ue08
    sleep 450s
done 

kubectl scale --replicas=0 deployment open5gs-ue01
kubectl scale --replicas=0 deployment open5gs-ue02
kubectl scale --replicas=0 deployment open5gs-ue03
kubectl scale --replicas=0 deployment open5gs-ue04
kubectl scale --replicas=0 deployment open5gs-ue05
kubectl scale --replicas=0 deployment open5gs-ue06
kubectl scale --replicas=0 deployment open5gs-ue07
kubectl scale --replicas=0 deployment open5gs-ue08
