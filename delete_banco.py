import pymysql.cursors

import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import create_engine


def obter_conexao():
    return pymysql.connect(
        host="172.16.22.76",
        user="admin",
        password="senaiead",
        database="cafeteria",
        # Retorna os resultados em formato de dicionário, facilitando consultas
        cursorclass=pymysql.cursors.DictCursor,)
con = obter_conexao()

engine = create_engine(
    "mysql+pymysql://admin:senaiead@172.16.22.76/cafeteria"
)


while True:
    print(f'''
      {60*'='}
      Digite
      [0]  opcover uma comanda inteira
      [1] para opcover um item de uma comanda
      [2] para cancelar a operação
      {60*'='}
''')
    opc = input('')

    try:
        int(opc)
    except:
        print('Opção inválida')
        continue
    
    if opc == 0:
        while True:
            cod = input('Insira a comanda a ser removida ou 0 para retornar ao menu: ')
            comandas = pd.read_sql_query('SELECT * FROM ComandaCliente')
            print(comandas.to_string(index=False))
            try:
                int(cod)
            except:
                print('Opção inválida!')
                continue

            with con.cursor() as cur:
                cur.execute(
                    """
                        SELECT * FROM ComandaCliente 
                        WHERE CodigoComanda = %s
                    """,(cod)
                )
                tem = cur.fetchone()
            if tem is None and tem!=0:
                print('Comanda não registrada')
                continue
            if tem == 0:
                break 

    elif opc == 1:
        cod = input('Insira a comanda a ser alterada ou 0 para retornar ao menu: ')
        try:
                int(cod)
            except:
                print('Opção inválida!')
                continue
        
        