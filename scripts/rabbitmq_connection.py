# coding=utf-8
###############################################################################
#
# Módulo python para criar conexáo com o RabbitMQ.
# 
# Parte do projeto para o módulo Serviços Cloud do treinamento Jornada Digital 
# ADA-Caixa
#
# Autor: Roberto Flavio Rezende
#
import pika


def new_connection(host='rabbitmq', vhost='projeto'):
    """ Função para estabelecer a conexão com o RabbitMQ

    Args:
        host (str): Endereço do RabbitMQ
        vhost (str): RabbitMQ virtual host a ser utilizado.

    Returns:
        object: Objeto de conexão ao RabbitMQ
    """
    with open('/run/secrets/usuario') as u:
        usuario = u.read()
    
    with open('/run/secrets/senha') as s:
        senha = s.read()
    
    conn_credentials = pika.PlainCredentials(username=usuario, password=senha)
    conn_parms = pika.ConnectionParameters(host=host, credentials=conn_credentials, virtual_host=vhost)
    connection = pika.BlockingConnection(conn_parms)
    return connection
