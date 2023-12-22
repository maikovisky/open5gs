kubectl get pods | grep Terminating | while read line; do
  pod_name=$(echo $line | awk '{print $1}' ) 
  kubectl delete pods $pod_name --grace-period=0 --force 
done
