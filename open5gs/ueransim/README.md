# UERAMSIM

[**UERANSIM**](https://github.com/aligungr/UERANSIM) (pronounced "ju-i ræn sɪm"), is the open source state-of-the-art 5G UE and RAN (gNodeB) simulator. UE and RAN can be considered as a 5G mobile phone and a base station in basic terms. The project can be used for testing 5G Core Network and studying 5G System.

[**UERANSIM**](https://github.com/aligungr/UERANSIM)  introduces the world's first and only open source 5G-SA UE and gNodeB implementation.


## GNode-B


### Files
Files used to deploy the gNB in a Kubernetes cluster.

- [gnb.yaml](gnb.yaml): Kubernet deplyment descriptor for gNB
- [gnb-init.yaml](gnb-init.yaml): Script for initContainer
- [gnb-configmap.yaml](gnb-configmap.yaml): Configmap with file nr-gnb config

## UE

### Files
Files used to deploy the UE in a Kubernetes cluster.

- [ue.yaml](ue.yaml): Kubernet deplyment descriptor for UE
- [ue-init.yaml](ue-init.yaml): Scripts for initContainer
  - [ueinit]: Script init UE                
  - [initUE.py]: Script for get IMSI for UE
- [ue-testing.yaml](ue-testing.yaml): Scripts for testing slices.