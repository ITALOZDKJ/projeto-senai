from datetime import datetime
import os  # <-- Para limpar a tela do terminal
from sqlalchemy import create_engine, text
import funcoes
import pandas as pd
import pymysql.cursors

con = funcoes.obter_conexao()
cur = con.cursor()

engine = create_engine(
    "mysql+pymysql://admin:senaiead@172.16.22.76/ferragens_do_ze"
)


# NOVA FUNÇÃO: Limpa o terminal para focar a atenção do usuário
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


# NOVA FUNÇÃO: Recarrega os dados para que o Pandas sempre veja o estoque atualizado
def atualizar_estoque_memoria():
    global estoque, ids_validos
    estoque = pd.read_sql_query("SELECT * FROM Produtos", engine)
    ids_validos = estoque["Id"].tolist()


# Inicializa os dados
atualizar_estoque_memoria()


def mostrar_menu():
    print(f'''
      {funcoes.mostrar_linha()}
      Ferragens do Zé - Frente de Caixa (Carrinho)
      {funcoes.mostrar_linha()}
      [0] Iniciar / Adicionar itens ao pedido
      [1] Fechar o carrinho (Concluir venda)
      [2] Cancelar o pedido (Limpar carrinho)
      [3] Remover um item específico
      [4] Exibir o carrinho atual
      [5] Sair do sistema
      {funcoes.mostrar_linha()}
''')


carrinho = []

while True:
    mostrar_menu()
    pag1 = input('Selecione a opção desejada: ').strip()

    # --------------------------------------------------
    # OPÇÃO 0: ADICIONAR ITENS AO CARRINHO
    # --------------------------------------------------
    if pag1 == '0':
        while True:
            limpar_tela()
            print("--- PRODUTOS EM ESTOQUE ---")
            print(estoque.to_string(index=False))
            print(funcoes.mostrar_linha())
            
            item = input('Selecione o ID do item ou -1 para retornar ao menu: ').strip()
            if item == '-1':
                break
            try:
                item = int(item)
            except ValueError:
                print('ID inválido! Use apenas números.')
                input('Pressione Enter para continuar...')
                continue    
            
            if item not in ids_validos:
                 print('Produto não encontrado no estoque!')
                 input('Pressione Enter para continuar...')
                 continue
                 
            while True:
                qtd = input('Insira a quantidade ou -1 para retornar: ').strip()
                if qtd == '-1':
                    break
                try:
                    qtd = int(qtd)
                except ValueError:
                    print('Quantidade inválida! Digite um número inteiro.')
                    continue
                
                nome = estoque.loc[estoque['Id'] == item, 'Nome'].values[0]
                em_estoque = estoque.loc[estoque['Id'] == item, 'Quantidade'].values[0]
                preco = estoque.loc[estoque['Id'] == item, 'Preco'].values[0] 
                categoria = estoque.loc[estoque['Id'] == item, 'Categoria'].values[0]
                
                if qtd <= 0 or qtd > em_estoque:
                    print(f'Quantidade indisponível! Em estoque: {em_estoque}')
                    input('Pressione Enter para ajustar...')
                    continue

                # CRUCIAL: Guardamos o 'Id' para conseguir dar o UPDATE depois!
                item_add = {
                    'Id': item,
                    'Nome': nome,
                    'Preço': preco,
                    'Quantidade': qtd,
                    'Categoria': categoria
                }

                carrinho.append(item_add)
                print(f'''
✔ Item adicionado com sucesso!
Item: {nome}   
Preço: R$ {preco:.2f}
Quantidade: {qtd}''')
                input('Pressione Enter para continuar comprando...')
                break  # Sai do loop da quantidade e volta para a listagem de produtos

    # --------------------------------------------------
    # OPÇÃO 1: FECHAR O CARRINHO (BAIXA NO BANCO DE DADOS)
    # --------------------------------------------------
    elif pag1 == '1':
        if not carrinho:
            print("\n Seu carrinho está vazio! Adicione itens primeiro.")
            input("Pressione Enter para voltar...")
            continue
            
        limpar_tela()
        print("--- FECHAMENTO DE PEDIDO ---")
        carrinho_df = pd.DataFrame(carrinho)
        print(carrinho_df[['Nome', 'Preço', 'Quantidade']].to_string(index=False))
        
        total = (carrinho_df['Preço'] * carrinho_df['Quantidade']).sum()
        print(f"\nTOTAL DO PEDIDO: R$ {total:.2f}")
        print(funcoes.mostrar_linha())
        
        # LOOP DE VALIDAÇÃO: Fica insistindo até o usuário digitar 1 ou 2
        while True:
            confirmar = input("Confirmar fechamento e atualizar estoque? (1-Sim / 2-Não): ").strip()
            if confirmar in ["1", "2"]:
                break  # Digitou certo? Sai do loop e segue para o if abaixo
            print("Opção inválida! Digite apenas 1 para Sim ou 2 para Não.\n")
        
        if confirmar == "1":
            # Abre a transação segura com o banco de dados
            with engine.begin() as conexao:
                for produto in carrinho:
                    # Coleta o estoque atual direto da memória do Pandas
                    qtd_atual = estoque.loc[estoque['Id'] == produto['Id'], 'Quantidade'].values[0]
                    nova_qtd = qtd_atual - produto['Quantidade']
                    
                    # Executa a query de atualização item por item
                    sql = text("UPDATE Produtos SET Quantidade = :nova_qtd WHERE Id = :id_item")
                    conexao.execute(sql, {"nova_qtd": nova_qtd, "id_item": produto['Id']})
            
            # Recarrega o Pandas para refletir as novas quantidades compradas
            atualizar_estoque_memoria()
            carrinho.clear() # Limpa o carrinho para a próxima venda
            print("\n✔ Venda concluída com sucesso e estoque atualizado!")
            input("Pressione Enter para retornar ao menu...")
        else:
            print("\n Fechamento cancelado. Itens mantidos no carrinho.")
            input("Pressione Enter para retornar...")

    # --------------------------------------------------
    # OPÇÃO 2: CANCELAR O PEDIDO
    # --------------------------------------------------
    elif pag1 == '2':
        if not carrinho:
            print("\nO carrinho já está vazio.")
        else:
            carrinho.clear()
            print("\n❌ Pedido cancelado e carrinho limpo com sucesso!")
        input("Pressione Enter para voltar...")

    # --------------------------------------------------
    # OPÇÃO 4: EXIBIR O CARRINHO
    # --------------------------------------------------
    elif pag1 == '4':
        limpar_tela()
        print("--- SEU CARRINHO ATUAL ---")
        if not carrinho:
            print("[ Vazio ]")
        else:
            carrinho_df = pd.DataFrame(carrinho)
            # Mostra colunas organizadas sem o index do Pandas poluindo
            print(carrinho_df[['Nome', 'Preço', 'Quantidade']].to_string(index=False))
            total = (carrinho_df['Preço'] * carrinho_df['Quantidade']).sum()
            print(f"\nValor parcial: R$ {total:.2f}")
        print(funcoes.mostrar_linha())
        input("Pressione Enter para retornar ao menu...")

    # --------------------------------------------------
    # OPÇÃO 5: SAIR DO SISTEMA
    # --------------------------------------------------
    elif pag1 == '5':
        limpar_tela()
        print('Saindo do programa... Até mais Zé!')
        break
        
    else:
        print("Opção inválida!")
        input("Pressione Enter para tentar novamente...")