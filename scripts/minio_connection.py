# coding=utf-8
###############################################################################
#
# Módulo python para criar conexáo com o MinIO.
# 
# Parte do projeto para o módulo Serviços Cloud do treinamento Jornada Digital 
# ADA-Caixa
#
# Autor: Roberto Flavio Rezende
#
from minio import Minio


def new_connection(host='minio'):
    """ Função para estabelecer a conexão com o MinIO

    Args:
        host (str): Endereço do MinIO.

    Returns:
        object: Objeto de conexão ao MinIO
    """
    with open('/run/secrets/usuario') as u:
        usuario = u.read()
    
    with open('/run/secrets/senha') as s:
        senha = s.read()
    
    client = Minio(f"{host}:9000",
        secure=False,
        access_key=usuario,
        secret_key=senha,
    )
    
    return client