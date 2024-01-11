# Cenário

O cenário imagino nesses experimentos é simular um transmissão de vídeo na qual o médico esteja operando a distância, para isso será necessário que o vídeo não tenha latência e tenha alta qualidade. Esse vídeo irá utilizar um slice específico para essa transmissão de vídeo (slice 1). O segundo slice foi imaginado diversos médicos e alunos assistindo a operação, o vídeo nesse caso não necessita muita qualidade e nem baixa latência. O terceiro slice será utilizado para a transmissão de mensagens de IoT de monitoramentos diversos. O quarto slice seria a simulação de um trafego de dados normal.

**anotações**: será que adicionar mais um slice para simular o uso de instrumentos remotamente (necessidade de baixa latencia)? Ou adicionar no mesmo slice 1 o tráfego de dados dos instrumentos. Ou o médico estará apenas orientando outro médico. 


# Experimentos


Os experimento iniciam com 1 UE para cada slice e vão subindo a cada 5 minutos o número de UEs em cada slice. 

| **Experience** |       **UPF1**      |       **UPF2**      |       **UPF3**      |       **UPF4**      |        **Obs**        |
|:--------------:|:-------------------:|:-------------------:|:-------------------:|:-------------------:|:---------------------:|
|     **01**     |   CPU: nd MEM: nd   |   CPU: nd MEM: nd   |   CPU: nd MEM: nd   |   CPU: nd MEM: nd   | Limintando banda UPF4 |
|     **02**     | CPU: 1250 MEM: 250  | CPU: 1200 MEM: 250  | CPU: 1200 MEM: 250  |   CPU: nd MEM: nd   | Limintando banda UPF4 |
|     **03**     | CPU: 1250 MEM: 250  |   CPU: nd MEM: nd   | CPU: 1250 MEM: 250  | CPU: 1250 MEM: 250  | Limintando banda UPF4 |
|                |                     |                     |                     |                     |                       |

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

Este experimento é composto por 4 slices, um UPF para cada slice, sendo que todos na mesma máquina. Somente o Slice 01 terá tráfego

### Slices

- **Slice 1** São 4 UEs. Enviando UDP de 32Mbps. Usando IPERF.
- **Slice 2** Recebendo UDP de 3Mbps. Usando IPERF.
- **Slice 3** Enviando mensagens MQTT a cada 1 segundo. Usando Mosquitto
- **Slice 4** Transmite dados TCP. Usando IPERF.

### Conclusões

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/bBqZSM6IMBazZhx3UyVmMi5ymp6JoJ3P)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/g5Gqo9ccySpTO70mbS6mODwROzJE1N4E)
- [Grafana](http://localhost:3000/goto/mLrE1XKIz?orgId=1)
- [GitHub - Tag vE01](https://github.com/maikovisky/open5gs/tree/vE01)


## Experimento 02 - Concorrento com um segundo Slice sem Limitações

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-2**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-3**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-4**
    - **Requests**: not defined
    - **Limits**: not defined

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/K5l4pTjHprz46f2FrwT9DYRLyuYQJDIA)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/pCCUitDnKYvbV1sAPqn5zloh9koqT6i7)
- [Grafana](http://localhost:3000/goto/2PlZbuKSk?orgId=1)


## Experimento 03 - Concorrento com todos os Slice sem Limitações

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-2**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-3**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-4**
    - **Requests**: not defined
    - **Limits**: not defined

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/IkpJj6BBfRaceIbRNhzhtyZZByaRCWBP)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/lS306605i2KmE3T67GDSKr4X7iy9fB9x)
- [Grafana](http://localhost:3000/goto/CxEbbXFSk?orgId=1)

## Experimento 04 - Recurso limitado para Slice 1

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: CPU 1000m
    - **Limits**: CPU 1000m
  - **UPF-2**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-3**
    - **Requests**: not defined
    - **Limits**: not defined
  - **UPF-4**
    - **Requests**: not defined
    - **Limits**: not defined

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/7OK2rSIxu4zwVPzIKvhdFv1D5b34vAkj)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/QSxpYcVB51711c2oSV5UirsassrbThsH)
- [Grafana](http://localhost:3000/goto/11FdS3FIk?orgId=1)


## Experimento 05 - Todos com recurso de CPU limitado

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: CPU 900m
    - **Limits**: CPU 900m
  - **UPF-2**
    - **Requests**: CPU 900m
    - **Limits**: CPU 900m
  - **UPF-3**
    - **Requests**: CPU 900m
    - **Limits**: CPU 900m
  - **UPF-4**
    - **Requests**: CPU 900m
    - **Limits**: CPU 900m

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/3zM7EcYldLvVcFQpGp6nOCaLFPcMON1c)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/dA4124mt2QO9jVtRJOAWAzxL1p4qrs1m)
- [Grafana](http://localhost:3000/goto/nvY77qFIz?orgId=1)


## Experimento 06 - Todos com recurso de CPU limitado, mas com mais recurso para slice 01

- Mesmo script do experimento 01, mas com limitação de recursos
  - **UPF-1**
    - **Requests**: CPU 1200m
    - **Limits**: CPU 1200m
  - **UPF-2**
    - **Requests**: CPU 900m
    - **Limits**: CPU 900m
  - **UPF-3**
    - **Requests**: CPU 800m
    - **Limits**: CPU 800m
  - **UPF-4**
    - **Requests**: CPU 600m
    - **Limits**: CPU 600m

###  Links: 
- [Snapshot raintank](https://snapshots.raintank.io/dashboard/snapshot/3zM7EcYldLvVcFQpGp6nOCaLFPcMON1c)
- [Snapshot local](http://localhost:3000/dashboard/snapshot/dA4124mt2QO9jVtRJOAWAzxL1p4qrs1m)
- [Grafana](http://localhost:3000/goto/nvY77qFIz?orgId=1)
