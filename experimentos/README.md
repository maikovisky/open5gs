# Experimentos

## Diagrama de rede

```mermaid
flowchart BT
    mac01["<b>mac-porvir-01</b>\nUPF1\nUPF2\nUPF3\nUPF4"]
    mac02["<b>mac-porvir-02</b>"\nIPERF-01]
    mac03["<b>mac-porvir-03</b>"\nIPERF-02]
    mac04["<b>mac-porvir-04</b>"\nIPERF-03]
    mac05["<b>mac-porvir-05</b>"\nIPERF-04]
    ue01["<b>mac-porvir-02</b>\nUE01"]
    ue02["<b>mac-porvir-03</b>\nUE02"]
    ue03["<b>mac-porvir-04</b>\nUE03"]
    ue04["<b>mac-porvir-05</b>\nUE04"]
    gn01["<b>mac-porvir-02</b>\nGNB01"]
    gn02["<b>mac-porvir-03</b>\nGNB02"]
    gn03["<b>mac-porvir-04</b>\nGNB03"]
    gn04["<b>mac-porvir-05</b>\nGNB04"]
    gn01--upf1-->mac01--iperf01-->mac02
    gn02--upf2-->mac01--iperf02-->mac03
    gn03--upf3-->mac01--iperf03-->mac04
    gn04--upf4-->mac01--iperf04-->mac05
    ue01--gnb01-->gn01
    ue02--gnb02-->gn02
    ue04--gnb03-->gn03
    ue03--gnb04-->gn04
    subgraph mac-porvir-01
      UPF1
      UPF2
      UPF3
      UPF4
    end
    subgraph mac-porvir-02
      UE01
      IPERF-01
    end
    subgraph mac-porvir-03
      UE02
      IPERF-02
    end
    subgraph mac-porvir-04
      UE03
      IPERF-03
    end
    subgraph mac-porvir-05
      UE04
      IPERF-04
    end
    UE01-->UPF1-->IPERF-01
    UE02-->UPF2-->IPERF-02
    UE03-->UPF3-->IPERF-03
    UE04-->UPF4-->IPERF-04
```

## Experimento 01 - Baseline

Este experimento é composto por 4 slices, um UPF para cada slice, sendo que todos na mesma máquina.  

- São 4 slices na mesma máquina.
- Rodando script que aumenta a cada 5 minutos o número de UEs para cada slice (2,3,4) na seguinte quantidade:
  -  {1,5,10,15,20,25,30}
- Todos slices sem restrição de recursos
- Após chegar a 30 UEs é reduzido a banda de UPF4 a cada 5 min
  - {100, 75, 50, 25, 10, 5, 1}

### Slices

- **Slice 1** não aumenta o número de UEs, fica fixo em um único UE. Recebnedo UDP de 32Mbps. Usando IPERF.
- **Slice 2** Recebendo UDP de 3Mbps. Usando IPERF.
- **Slice 3** Enviando mensagens MQTT a cada 1 segundo. Usando Mosquitto
- **Slice 4** Transmite dados TCP. Usando IPERF.

### Conclusões

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/6D7ZVa1knxh0uAnkTCJr7puoE4ETT6tS)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/r4OTaQXUt0F2h0YiSDWkv5Oyz5lmKQTX)
- [GitHub - Tag vE01](https://github.com/maikovisky/open5gs/tree/vE01)

## Experimento 02 - Limitando recursos

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: CPU 1250m, MEM: 250m
    - **Limits**: CPU 1250m, MEM: 250m
  - **UPF-2**
    - **Requests**: CPU 1200m, MEM: 250m
    - **Limits**: CPU 1200m, MEM: 250m
  - **UPF-3**
    - **Requests**: CPU 1200m, MEM: 250m
    - **Limits**: CPU 1200m, MEM: 250m
  - **UPF-4**
    - **Requests**: not defined
    - **Limits**: not defined

### Conclusões

### Links:
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/0NB01YiXKN5ucm71tFOdiI9pLLmrPI1C)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/J1H7PIhXANeCujItO6XqTuexcxohXoy6)