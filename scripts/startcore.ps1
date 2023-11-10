kubectl scale --replicas=1 deployment open5gs-nrf
kubectl scale --replicas=1 deployment open5gs-amf
# kubectl scale --replicas=1 deployment open5gs-amf2
kubectl scale --replicas=1 deployment open5gs-ausf
kubectl scale --replicas=1 deployment open5gs-bsf
kubectl scale --replicas=1 deployment open5gs-nssf
kubectl scale --replicas=1 deployment open5gs-pcf
kubectl scale --replicas=1 deployment open5gs-scp
kubectl scale --replicas=1 deployment open5gs-smf
kubectl scale --replicas=1 deployment open5gs-udm
kubectl scale --replicas=1 deployment open5gs-udr
kubectl scale --replicas=1 deployment open5gs-smf

Start-Sleep -s 15

kubectl scale --replicas=1 deployment open5gs-upf-1
kubectl scale --replicas=1 deployment open5gs-upf-2
kubectl scale --replicas=1 deployment open5gs-upf-3
kubectl scale --replicas=1 deployment open5gs-upf-4
# kubectl scale --replicas=1 deployment open5gs-upf-5
# kubectl scale --replicas=1 deployment open5gs-upf-6
# kubectl scale --replicas=1 deployment open5gs-upf-7
# kubectl scale --replicas=1 deployment open5gs-upf-8

Start-Sleep -s 15

kubectl scale --replicas=1 deployment open5gs-ueransim01
kubectl scale --replicas=1 deployment open5gs-ueransim02
kubectl scale --replicas=1 deployment open5gs-ueransim03
kubectl scale --replicas=1 deployment open5gs-ueransim04
kubectl scale --replicas=1 deployment open5gs-ueransim05
kubectl scale --replicas=1 deployment open5gs-ueransim06
kubectl scale --replicas=1 deployment open5gs-ueransim07
kubectl scale --replicas=1 deployment open5gs-ueransim08




