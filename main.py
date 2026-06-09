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
      comanda_df = pd.DataFrame(comanda) # Renamed 'comanda' variable to avoid shadowing
      print(comanda_df)
      con = funcoes.obter_conexao()
      cur = con.cursor()
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
    break

  elif pedido == -2:
    print('Pedido cancelado.')
    comanda.clear()
    break

  elif pedido == -3:
      if len(comanda) == 0:
        print('Não há pedidos no momento.')
      elif len(comanda) == 1:
        comanda.pop()
        print('Último item removido')
      else:
        while True:
          for item, linha in enumerate(comanda):
            print(f'{item+1} - {linha["Nome"]}')
          item_rem = input('Digite o numero do item a ser removido ou -1 para retornar ao menu: ')

          try:
            item_rem = int(item_rem)
          except:
            print('Opção inválida')
            continue
          item_rem = int(item_rem)
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