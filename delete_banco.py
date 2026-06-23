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
      [0]  remover uma comanda inteira
      [1] para remover um item de uma comanda
      [2] para cancelar a operação
      {60*'='}
''')
    opc = input('')

    try:
        opc = int(opc)
    except:
        print('Opção inválida')
        continue
    
    if opc == 0:
        while True:
            
            comandas = pd.read_sql_query('SELECT * FROM ComandaCliente', engine)
            print(comandas.to_string(index=False))
            cod = input('Insira a comanda a ser removida ou 0 para retornar ao menu: ')

            try:
                cod = int(cod)
            except:
                print('Opção inválida!')
                continue
            if cod == 0:
                break 
            with con.cursor() as cur:
                cur.execute(
                    """
                        SELECT * FROM ComandaCliente 
                        WHERE CodigoComanda = %s
                    """,(cod,)
                )
                tem = cur.fetchone()
            if tem is None:
                print('Comanda não registrada')
                continue
            
            with con.cursor() as cur:

                cur.execute(
                    "DELETE FROM Comanda WHERE Codigo_Pedido = %s",
                    (cod,)
                )

                cur.execute(
                    "DELETE FROM ComandaCliente WHERE CodigoComanda = %s",
                    (cod,)
                )

                con.commit()

            print('Comanda removida com sucesso.')

    elif opc == 1:
        while True:
            comandas = pd.read_sql_query('SELECT * FROM ComandaCliente', engine)
            print(comandas.to_string(index=False))
            
            cod = input('Insira a comanda a ser alterada ou 0 para retornar ao menu: ')
            try:
                cod = int(cod)
            except:
                print('Opção inválida!')
                continue
            if cod == 0:
                break 
            with con.cursor() as cur:
                cur.execute(
                    """
                        SELECT * FROM ComandaCliente 
                        WHERE CodigoComanda = %s
                    """,(cod,)
                )
                tem = cur.fetchone()
            if tem is None:
                print('Comanda não registrada')
                continue
            
            while True:
            
                comandas = pd.read_sql_query(f'SELECT * FROM Comanda WHERE Codigo_Pedido = {cod}', engine)
                
                print(f'{"ITEM":<6}{"PRODUTO":<20}{"QTD":<5}')
                print('=' * 31)

                for indice, linha in enumerate(comandas.itertuples(), start=1):
                    print(
                        f'{indice:<6}'
                        f'{linha.Nome:<20}'
                        f'{linha.Quantidade:<5}'
                    )
                item = input('Selecione o item a ser alterado ou -1 para retornar ao menu: ')
                
                try:
                    item = int(item)
                except:
                    print('Item inválido')
                    continue
                
                if item == -1:
                    break

                if item-1 not in comandas.index:
                    print('Item inválido blabla')
                    continue
                

                qtdd = input('Informe a quantidade ou -1 para voltar: ')

                try:
                    qtdd = int(qtdd)
                except:
                    print('Quantidade inválida')
                    continue

                
                if qtdd == -1:
                    continue

                if qtdd <= 0:
                    print('Quantidade inválida')
                    continue

                
                linha = comandas.iloc[item - 1]


               # linha = comandas.iloc[item]
                quantidade_atual = linha['Quantidade']
                nome = linha['Nome']
                valor_unitario = linha['Valor_Unitario']

                if qtdd > quantidade_atual:
                    print('Quantidade maior que a registrada na comanda.')
                    continue

                nova_quantidade = quantidade_atual - qtdd

                if nova_quantidade == 0:

                    with con.cursor() as cur:
                        cur.execute(
                            """
                            DELETE FROM Comanda
                            WHERE Codigo_Pedido = %s
                            AND Nome = %s
                            """,
                            (cod, nome)
                        )

                    con.commit()

                else:

                    with con.cursor() as cur:
                        cur.execute(
                            """
                            UPDATE Comanda
                            SET Quantidade = %s
                            WHERE Codigo_Pedido = %s
                            AND Nome = %s
                            """,
                            (
                                nova_quantidade,
                                cod,
                                nome
                            )
                        )

                    con.commit()


                itens = pd.read_sql_query(
                    f'SELECT * FROM Comanda WHERE Codigo_Pedido = {cod}',
                    engine
                )

                novo_total = (
                    itens['Quantidade'] *
                    itens['Valor_Unitario']
                ).sum()

                if len(itens) == 0:

                    with con.cursor() as cur:
                        cur.execute(
                            """
                            DELETE FROM ComandaCliente
                            WHERE CodigoComanda = %s
                            """,
                            (cod,)
                        )

                    con.commit()

                    print('Último item removido e comanda apagada.')
                    break
                else:

                    with con.cursor() as cur:
                        cur.execute(
                            """
                            UPDATE ComandaCliente
                            SET Valor = %s
                            WHERE CodigoComanda = %s
                            """,
                            (float(novo_total), cod)
                        )

                    con.commit()

                    print('Quantidade atualizada.')
    elif opc == 2:
        break

    else:
        print('Opção inválida:')
        continue
