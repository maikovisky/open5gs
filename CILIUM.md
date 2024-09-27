

[Tutorial para Migração](https://isovalent.com/blog/post/tutorial-migrating-to-cilium-part-1/#:~:text=Tutorial%3A%20How%20to%20Migrate%20to%20Cilium%20%28Part%201%29,5%20Step%205%20%E2%80%93%20Start%20the%20Migration%20)


[Laboratório para Migração](https://isovalent.com/labs/migrating-to-cilium/)


## Disable Hubble
helm upgrade cilium cilium/cilium --version 1.16.1 --namespace=kube-system   --reuse-values --set hubble.enabled=false --set hubble.relay.enabled=false --set hubble.ui.enabled=false

## Enable routingMode=native
helm upgrade cilium cilium/cilium --version 1.16.1 --namespace=kube-system   --reuse-values --set routingMode=native