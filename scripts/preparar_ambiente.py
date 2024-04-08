# coding=utf-8
###############################################################################
#
# Script para preparar o ambiente do Projeto
#
# Parte do projeto do módulo Conteinerização do treinamento Jornada Digital 
# ADA-Caixa
#
# Autor: Roberto Flavio Rezende
#
import json
import redis
import random
from datetime import datetime
from minio_connection import new_connection as minio_con
from rabbitmq_connection import new_connection as rabbitmq_con


def write_out(msg):
    """ Print no log do Docker

    Args:
        msg (str): Mensagem a ser impressa
    """
    mascara_timestamp = '%Y-%m-%d %H:%M:%S'
    timestamp = datetime.strftime(datetime.now(), mascara_timestamp)
    print(f'{timestamp} {msg}')
    

def create_rbbitmq():
    """ Prepara o ambiente do RabbitMQ.
        Cria a exchange, a fila para as transações e faz o bind entre elas.
    """
    write_out('Preparando ambiente do RabbitMQ.')
    con = rabbitmq_con()
    channel = con.channel()

    channel.exchange_declare(exchange='transacoes', exchange_type='direct')

    # Fila para as transações
    channel.queue_declare(queue='transacoes_solicitadas', durable=True)
    channel.queue_bind(queue='transacoes_solicitadas', exchange='transacoes', routing_key='solicitar')

    con.close()

    write_out(f'Ambiente do RabbitMQ pronto.')


def create_minio():
    """ Prepara o ambiente do MinIO.
        Cria o bucket para receber os relatórios e configura a política de segurança.
    """
    write_out('Preparando ambiente do MinIO.')
    client = minio_con()

    bucket_name = 'relatorios-fraudes'

    bucket_found = client.bucket_exists(bucket_name)
    if not bucket_found:
        write_out(f'Bucket {bucket_name} não existe. Criando.')
        client.make_bucket(bucket_name)

        # Permite a leitura dos relatórios sem necessidade de autenticação.
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "*"
                        ]
                    },
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*"
                    ]
                }
            ],
        }
        
        client.set_bucket_policy(bucket_name, json.dumps(policy))

        write_out(f'Bucket {bucket_name} criado no MinIO.')
    
    write_out(f'Ambiente do MinIO pronto.')
    
    
def create_redis():
    """ Prepara o ambiente do Redis.
        Gera 20 contas aleatórias.
        Cria uma lista com as contas no Redis.
        Cria uma entrada do tipo lista para cada conta no Redis
    """
    r = redis.Redis(host='redis', port=6379, decode_responses=True, )

    write_out(f'Preparando o ambiente do Redis.')

    quantidade_de_contas = 20

    # Função para gerar o número da conta
    criar_conta = lambda x: f'{random.randrange(10000, 99999)}-{random.randrange(1, 9)}'
    lista_contas = [criar_conta(None) for i in range(quantidade_de_contas)]
    
    r.rpush('contas', *lista_contas)

    write_out(f'Contas a serem criadas: {lista_contas}')

    for conta in lista_contas:
        r.json().set(conta, '$', {'transacoes': []})

    write_out(f'Ambiente do Redis pronto.')
    

def main():
    """ Main ;)
    """
    write_out('Preparando o ambiente do projeto.')
    create_rbbitmq()
    create_minio()
    create_redis()
    write_out('Ambiente do projeto pronto para utilização.')

if __name__ == '__main__':
    main()
    