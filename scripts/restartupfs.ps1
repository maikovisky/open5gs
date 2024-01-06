
kubectl scale --replicas=0 deployment open5gs-ueransim01
kubectl scale --replicas=0 deployment open5gs-ueransim02
kubectl scale --replicas=0 deployment open5gs-ueransim03
kubectl scale --replicas=0 deployment open5gs-ueransim04


kubectl scale --replicas=0 deployment open5gs-upf-1
kubectl scale --replicas=0 deployment open5gs-upf-2
kubectl scale --replicas=0 deployment open5gs-upf-3
kubectl scale --replicas=0 deployment open5gs-upf-4


Start-Sleep -s 15

kubectl scale --replicas=1 deployment open5gs-upf-1
kubectl scale --replicas=1 deployment open5gs-upf-2
kubectl scale --replicas=1 deployment open5gs-upf-3
kubectl scale --replicas=1 deployment open5gs-upf-4


Start-Sleep -s 15

kubectl scale --replicas=1 deployment open5gs-ueransim01
kubectl scale --replicas=1 deployment open5gs-ueransim02
kubectl scale --replicas=1 deployment open5gs-ueransim03
kubectl scale --replicas=1 deployment open5gs-ueransim04
