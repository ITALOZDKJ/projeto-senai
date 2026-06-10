#Execução do código

import pymysql.cursors
import funcoes
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import create_engine

#Funções


con = funcoes.obter_conexao()
cur = con.cursor()

engine = create_engine(
    "mysql+pymysql://admin:senaiead@172.16.22.76/cafeteria"
)

cardapio = pd.read_sql_query(
    "SELECT * FROM Produtos",
    engine
)

ultima_comanda = pd.read_sql_query(
    "SELECT MAX(CodigoComanda) AS Codigo FROM ComandaCliente",
    engine
)

ultimo_codigo = ultima_comanda["Codigo"].iloc[0]

if pd.isna(ultimo_codigo):
    codigo_comanda = 1
else:
    codigo_comanda = int(ultimo_codigo) + 1
comanda = []

print(cardapio.to_string(index=False))

funcoes.mostrar_menu()

con.close()

while True:

  pedido = input('Digite o item: ')

  try:
      pedido = int(pedido)

  except:
      print('Opção inválida')
      continue

  

  

  if pedido-1 in list(cardapio.index):
    preco = cardapio.loc[pedido-1,'preco']
    nome = cardapio.loc[pedido-1,'nome']
    funcoes.adicionar_item(comanda, nome, preco, codigo_comanda)



  elif pedido == 0:
    funcoes.mostrar_comanda(comanda)

  elif pedido == -1:
    if len(comanda) == 0:
      print('Não há pedidos no momento.')
      continue
    else:
      print('Fechando pedido...')
      
      funcoes.fechar_comanda(comanda, codigo_comanda)
      break


  elif pedido == -2:
    print('Pedido cancelado.')
    comanda.clear()
    break

  elif pedido == -3:
    if len(comanda) == 0:
      print('Não há pedidos no momento.')
    elif len(comanda) == 1:
      if comanda[0]['Quantidade'] == 1:
        comanda.pop()
        print('Item removido')
      else:
        
        while True:

          print(f'{"ITEM":<6}{"PRODUTO":<30}{"QTD":<5}')
          print('=' * 41)

          for item, linha in enumerate(comanda):
              print(
                  f'{item+1:<6}'
                  f'{linha["Nome"]:<30}'
                  f'{linha["Quantidade"]:<5}'
              )
          item_rem = input('Digite o numero do item a ser removido ou -1 para retornar ao menu: ')

          try:
            item_rem = int(item_rem)
          except:
            print('Opção inválida')
            continue
          if item_rem == -1:
            funcoes.mostrar_menu()
            break
          elif item_rem not in range(1,len(comanda)+1):
            print('Opção inválida')
            continue
          else:
            for item in comanda:
              if item['Nome'] == comanda[item_rem-1]['Nome']:
                if item['Quantidade'] == 1:
                  comanda.remove(item)
                else:
                  item['Valor'] -= item['Valor']/item['Quantidade']
                  item['Quantidade'] -= 1
                  break






  else:
    print('Opção inválida, digite outra')
    continue
    con.commit()
    con.close()