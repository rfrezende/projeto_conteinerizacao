# coding=utf-8
###############################################################################
#
# Script para enviar solicitações de transações para o RabbitMQ
#
# Parte do projeto do módulo Serviços Cloud do treinamento Jornada Digital 
# ADA-Caixa
#
# Autor: Roberto Flavio Rezende
#
import json
import redis
import random
from rabbitmq_connection import new_connection
from time import sleep
from datetime import datetime


timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
print(f'{timestamp} Iniciando a produção de transações...')

r = redis.Redis(host='redis', port=6379, decode_responses=True)
contas = r.lrange('contas', 0, -1)

connection = new_connection()
channel = connection.channel()

while True:
    # Sem o sleep o script iria gerar milhares de transações por segundo e moer a CPU.
    sleep(2)
    
    # Coloca todas as transacoes no em Sao Paulo e 10% para Rio de Janeiro com o intuito de gerar "fraude"
    cidade = 'Rio de Janeiro' if random.random() < 0.1 else 'Sao Paulo'
    
    # Escolhe uma conta aleatoriamente para enviar a transação
    conta_origem = contas[random.randint(0, len(contas) - 1)]
    conta_destino = contas[random.randint(0, len(contas) - 1)]
    
    # Escolhe um valor aleatório para a transação.
    # Não serve para nada, mas porque não fazer?
    valor = random.randrange(100, 5000)
    
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    transacao = {'conta': conta_origem, 'transacao': {'conta_destino': conta_destino, 'valor': valor, 'cidade': cidade, 'timestamp': timestamp}}
    channel.basic_publish(exchange='transacoes', routing_key='solicitar', body=json.dumps(transacao))
    print(transacao)