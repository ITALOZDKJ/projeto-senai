#Execução do código

import pymysql.cursors

import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
from sqlalchemy import create_engine

def mostrar_linha():
  print('=' *60)

def obter_conexao():
    return pymysql.connect(
        host="172.16.22.76",
        user="admin",
        password="senaiead",
        database="cafeteria",
        # Retorna os resultados em formato de dicionário, facilitando consultas
        cursorclass=pymysql.cursors.DictCursor,)
con = obter_conexao()
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
print(f'''
      {mostrar_linha()}
      Selecione uma opção do cardápio, ou umas das opções a seguir:
      [0]  para ver a comanda
      [-1] para fechar o pedido
      [-2] para cancelar o pedido
      [-3] para remover um item
      {mostrar_linha()}
''')
con.close()

opcoes = [-3.-2,-1,0]
while True:
  pedido = input('Digite o item: ')
  try:
    pedido = int(pedido)

  except:
    print('Opção inválida')
    continue
  pedido = int(pedido)
  if pedido-1 in list(cardapio.index):
    preco = cardapio.loc[pedido-1,'preco']
    nome = cardapio.loc[pedido-1,'nome']
    ja_esta = False
    for pedido_item in comanda: # Renamed 'pedido' variable to avoid shadowing
      if pedido_item['Nome'] == nome:
        pedido_item['Quantidade'] += 1
        pedido_item['Valor'] += preco
        ja_esta = True
    if not ja_esta:
      comanda.append({'Nome': nome, 'Quantidade': 1, 'Valor': preco, 'Cod Comanda': codigo_comanda })
  elif pedido == 0:
    if len(comanda) == 0:
      print('Não há pedidos no momento.')
    else:
      comanda_df = pd.DataFrame(comanda)
      print(comanda_df)
      print(f'O valor da conta está em R${comanda_df["Valor"].sum()}')

  elif pedido == -1:
    if len(comanda) == 0:
      print('Não há pedidos no momento.')
      continue
    else:
      print('Fechando pedido...')
      comanda_df = pd.DataFrame(comanda) # Renamed 'comanda' variable to avoid shadowing
      print(comanda_df)
      con = obter_conexao()
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
            print(f'''
                      {mostrar_linha()}
                      Selecione uma opção do cardápio, ou umas das opções a seguir:
                      [0]  para ver a comanda
                      [-1] para fechar o pedido
                      [-2] para cancelar o pedido
                      [-3] para remover um item
                      {mostrar_linha()}
                  ''')
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