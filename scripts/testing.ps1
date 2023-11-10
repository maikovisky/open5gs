

#$numbers=0,1,5,10,20,30,40,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775
$numbers=1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50
foreach ($num in $numbers) {
    $num;
    kubectl scale --replicas=$num deployment open5gs-ue01
    kubectl scale --replicas=$num deployment open5gs-ue02
    kubectl scale --replicas=$num deployment open5gs-ue03
    kubectl scale --replicas=$num deployment open5gs-ue04
    kubectl scale --replicas=$num deployment open5gs-ue05
    kubectl scale --replicas=$num deployment open5gs-ue06
    kubectl scale --replicas=$num deployment open5gs-ue07
    kubectl scale --replicas=$num deployment open5gs-ue08
    Start-Sleep -s 450
 }

kubectl scale --replicas=0 deployment open5gs-ue01
kubectl scale --replicas=0 deployment open5gs-ue02
kubectl scale --replicas=0 deployment open5gs-ue03
kubectl scale --replicas=0 deployment open5gs-ue04
kubectl scale --replicas=0 deployment open5gs-ue05
kubectl scale --replicas=0 deployment open5gs-ue06
kubectl scale --replicas=0 deployment open5gs-ue07
kubectl scale --replicas=0 deployment open5gs-ue08