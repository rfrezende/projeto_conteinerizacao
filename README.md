
# Projeto do Módulo *Serviços Cloud*

## Treinamento Jornada Digital ADA-Caixa

### Descrição:

Solução proposta para o projeto do módulo *Serviços Cloud* do treinamento Jornada Digital Devops ADA-Caixa.  

A solução foi encapsulada totalmente em containers e executa tudo na ordem correta. Foi testada em ambiente Debian, WSL com Ubuntu, Amazon Linux e Fedora Server.

Os scripts executam em containers próprios como a seguir:

- `criar_contas_redis.py`: Cria os objetos JSON com os números das contas e uma lista de transações no Redis. Ele executa e para o container.
- `criar_ambiente_rabbitmq.py`: Cria a exchange, a fila e o biding no RabbitMQ. Ele executa e para o container.
- `criar_ambiente_minio.py`: Cria o bucket no MinIO. Ele executa e para o container.
- `producer_transacoes.py`: Gera transaçoes aleatórias e envia para o RabbitMQ.
- `consumer_transacoes.py`: Consome a fila no RabbitMQ, grava o cache e gera o relatório de fraude, caso seja identificado.

Os demais containers são os serviços do Minio, RabbitMQ, Redis e funções auxiliares.  

O critério para fraude foi a mudança de cidades em um intervalo menor do que duas horas.  
  
  
### Instruções:

1. Instalar o Docker e o Docker Compose.  

    - [https://docs.docker.com/engine/install/ ](https://docs.docker.com/engine/install/ ) 
    - [https://docs.docker.com/compose/install/standalone/](https://docs.docker.com/compose/install/standalone/)  

2. Instalar o git (a partir daqui os passos deverão ser realizados apenas em ambiente Linux ou WSL).

    - https://git-scm.com/book/en/v2/Getting-Started-Installing-Git  

4. Clonar o repositório para seu laboratório  

```
git clone https://github.com/rfrezende/projeto_servicos_cloud.git  
```

5. Executar o ambiente [^bignote].  

```
cd projeto_servicos_cloud
```
```
sudo docker image build --tag projeto_ada:latest --file ./base_scripts.Dockerfile .
```
```
sudo docker-compose up -d
```  

6. Verificar os logs do container que gera o relatório. Pode demorar alguns minutos para aparecer uma "fraude".  

```
sudo docker logs --follow consumer_transacoes  
```

7. Remover o laboratório.  

```
sudo docker-compose down  
```
```
cd ..  
```
```
sudo rm -r projeto_servicos_cloud  
```
```
sudo docker rmi projeto_ada minio/minio redis/redis-stack rabbitmq:3-management $(sudo docker images | grep 'none' | awk '{print $3}')
```  
  
  
  
[^bignote]: Se tiver problemas com o Fedora ou outra distribuição baseada em Red Hat, execute o comando abaixo antes do docker-compose  
    `sudo setenforce 0`
