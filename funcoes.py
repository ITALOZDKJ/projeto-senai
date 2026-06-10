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



def fechar_comanda(comanda, codigo_comanda):
        comanda_df = pd.DataFrame(comanda) 
        print(comanda_df)
        con = obter_conexao()
        total = comanda_df['Valor'].sum()
        data = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime("%d/%m/%Y")
        hora = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime("%H:%M")
        print(f'O valor da conta ficou em R${total}')
        with con.cursor() as cur:
          cur.execute("""
                    INSERT INTO ComandaCliente (Valor, Data, Hora, CodigoComanda)
                    VALUES (%s, %s, %s,%s)""",
                    (total, data, hora, codigo_comanda)

            )
        for item, linha in comanda_df.iterrows():
          with con.cursor() as cur:
            cur.execute(
                '''INSERT INTO Comanda (Nome, Quantidade, Valor_Unitario, Codigo_Pedido) VALUES (%s, %s, %s,%s)''',
                (linha['Nome'], linha['Quantidade'], linha['Valor']/linha['Quantidade'], linha['Cod Comanda'])
            )
        

        con.commit()
        con.close()

