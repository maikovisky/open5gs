
# Comandos Kubectl

Pega IP dos PODs
```
kubectl get pod -o wide | grep iperf
```


# Comandos Cilium

```
 kubectl exec -it -n kube-system cilium-8vlb6 -- cilium-dbg bpf bandwidth list
```



# Comandos TC

Comando para listar qdisc 
```
ls /sys/class/net | xargs -i sh -c 'echo "--------\n"{} && tc -s qdisc show dev {}'
```


# Comando Helm

```
helm upgrade cilium cilium/cilium --version 1.16.1 --namespace=kube-system   --reuse-values --set ...
kubectl rollout restart deploy cilium-operator -n kube-system
kubectl -n kube-system rollout restart ds/cilium
```