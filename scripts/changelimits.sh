

#kubectl patch deployment open5gs-upf-1 -p '{"spec":{"template":{"spec":{"containers":[{"name":"upf1", "resources":{"requests":{"cpu":"950m", "memory": "250Mi"}, "limits":{"cpu": "950m", "memory": "250Mi"}}}]}}}}'
#kubectl patch deployment open5gs-upf-2 -p '{"spec":{"template":{"spec":{"containers":[{"name":"upf2", "resources":{"requests":{"cpu":"950m", "memory": "250Mi"}, "limits":{"cpu": "950m", "memory": "250Mi"}}}]}}}}'
#kubectl patch deployment open5gs-upf-3 -p '{"spec":{"template":{"spec":{"containers":[{"name":"upf3", "resources":{"requests":{"cpu":"950m", "memory": "250Mi"}, "limits":{"cpu": "950m", "memory": "250Mi"}}}]}}}}'
#kubectl patch deployment open5gs-upf-4 -p '{"spec":{"template":{"spec":{"containers":[{"name":"upf4", "resources":{"requests":{"cpu":"950m", "memory": "250Mi"}, "limits":{"cpu": "950m", "memory": "250Mi"}}}]}}}}'

changeLimits() {
  UPF=$1
  CPU=$2
  MEM=$3

  #c="{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"upf$UPF\", \"resources\":{\"requests\":{\"cpu\":\"$CPU\", \"memory\": \"$MEM\"}, \"limits\":{\"cpu\":\"$CPU\", \"memory\": \"$MEM\"}}}]}}}}" 
  c='{"spec":{"template":{"spec":{"containers":[{"name":"upf'$UPF'", "resources":{"requests":{"cpu":"'$CPU'", "memory": "'$MEM'"}, "limits":{"cpu":"'$CPU'", "memory": "'$MEM'"}}}]}}}}' 

  echo $c
  kubectl scale --replicas=0 deployment open5gs-upf-$UPF
  kubectl patch deployment open5gs-upf-$UPF -p "$c"
  kubectl get pods  open5gs-upf-$UPF 
  while a=$(kubectl get pods | grep Running | grep upf- | wc -l) 
  do
    if [ $a -le 4 ] 
    then
	continue
    fi
  done
}
changeLimits 1 0 0 



