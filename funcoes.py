import pymysql.cursors

import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import create_engine

def mostrar_linha():
  return '=' * 60

def mostrar_menu():
  print(f'''
      {mostrar_linha()}
      Selecione uma opção do cardápio, ou umas das opções a seguir:
      [0]  para ver a comanda
      [-1] para fechar o pedido
      [-2] para cancelar o pedido
      [-3] para remover um item
      {mostrar_linha()}
''')

def obter_conexao():
    return pymysql.connect(
        host="172.16.22.76",
        user="admin",
        password="senaiead",
        database="cafeteria",
        # Retorna os resultados em formato de dicionário, facilitando consultas
        cursorclass=pymysql.cursors.DictCursor,)

def adicionar_item(comanda, nome, preco, codigo_comanda):
    for item in comanda:
        if item['Nome'] == nome:
            item['Quantidade'] += 1
            item['Valor'] += preco
            return

    comanda.append({
        'Nome': nome,
        'Quantidade': 1,
        'Valor': preco,
        'Cod Comanda': codigo_comanda
    })

def mostrar_comanda(comanda):

    if not comanda:
        print('Não há pedidos no momento.')
        return

    comanda_df = pd.DataFrame(comanda)

    print(comanda_df)
    print(f'O valor da conta está em R${comanda_df["Valor"].sum()}')