
## Experimento 1

São 4 slices, onde cada slice tem 1 gNodeB, 1 UPF e 1 servidor IPERF.

Cada UE tem 3 conteiner

* Um de inicialização para as confiurações.
* Um para conectar com o gNodeB
* Um para os testes
  - Espera 15 segundos para a UE conectar
  - Roda o IPERF por 5 minutos
  - Espera por 120 segundos e roda o IPERF novamente


A cada 360 segundos é acrescentado um UE para cada slice. Quando atingir 10 UEs sobe de 5 em 5 até atingir 50 UEs por slice.