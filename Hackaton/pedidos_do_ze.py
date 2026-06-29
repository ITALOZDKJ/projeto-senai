
from datetime import datetime
import os  # Biblioteca utilizada para interagir com o sistema operacional (limpeza de terminal)
from sqlalchemy import create_engine, text  # Usado para criar conexões e estruturar comandos SQL de forma segura
import Hackaton.funcoes as funcoes  # Módulo personalizado contendo funções utilitárias do sistema
import pandas as pd  # Usado para manipular e visualizar tabelas de dados na memória
import pymysql.cursors  # Driver para realizar a ponte de comunicação com o banco MySQL

# Inicialização de variáveis globais de conexão (utilizadas por funções externas)
con = funcoes.obter_conexao()
cur = con.cursor()

# Cria o mecanismo de conexão (Engine) do SQLAlchemy para o banco de dados "ferragens_do_ze"
engine = create_engine(
    "mysql+pymysql://admin:senaiead@172.16.22.76/ferragens_do_ze"
)


# FUNÇÃO: Limpa o console do terminal para organizar as telas visualmente
def limpar_tela():
    # 'cls' para sistemas Windows (nt), 'clear' para sistemas baseados em Unix (Linux/Mac)
    os.system("cls" if os.name == "nt" else "clear")


# FUNÇÃO: Recarrega a base de dados do MySQL direto na memória do DataFrame do Pandas
def atualizar_estoque_memoria():
    global estoque, ids_validos  # Escancara as variáveis para acesso global no script
    # Consulta a tabela inteira e converte em DataFrame
    estoque = pd.read_sql_query("SELECT * FROM Produtos", engine)
    # Transforma a coluna de IDs em uma lista nativa do Python para checagens com o operador 'in'
    ids_validos = estoque["Id"].tolist()


# Executa a carga inicial dos dados assim que o script é iniciado
atualizar_estoque_memoria()


# FUNÇÃO: Exibe as opções textuais da Frente de Caixa no terminal
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


# Inicializa uma lista vazia que servirá como estrutura de dados temporária para o carrinho
carrinho = []

# Loop principal do menu do sistema de caixa
while True:
    mostrar_menu()
    # Captura a entrada limpando possíveis espaços em branco digitados nas pontas (.strip())
    pag1 = input('Selecione a opção desejada: ').strip()

    # --------------------------------------------------
    # OPÇÃO 0: ADICIONAR ITENS AO CARRINHO
    # --------------------------------------------------
    if pag1 == '0':
        while True:
            limpar_tela()
            print("--- PRODUTOS EM ESTOQUE ---")
            # Exibe o estoque em formato string, escondendo os índices autogerados do Pandas
            print(estoque.to_string(index=False))
            print(funcoes.mostrar_linha())
            
            item = input('Selecione o ID do item ou -1 para retornar ao menu: ').strip()
            if item == '-1':
                break
                
            # Tenta converter a entrada do ID para inteiro
            try:
                item = int(item)
            except ValueError:
                print('ID inválido! Use apenas números.')
                input('Pressione Enter para continuar...')
                continue    
            
            # Verifica se o ID inserido existe no banco consultando nossa lista na memória
            if item not in ids_validos:
                 print('Produto não encontrado no estoque!')
                 input('Pressione Enter para continuar...')
                 continue
                 
            # Sub-loop para coletar e validar a quantidade do item desejado
            while True:
                qtd = input('Insira a quantidade ou -1 para retornar: ').strip()
                if qtd == '-1':
                    break
                try:
                    qtd = int(qtd)
                except ValueError:
                    print('Quantidade inválida! Digite um número inteiro.')
                    continue
                
                # Coleta pontualmente as informações do produto direto do DataFrame usando indexação condicional (.loc)
                nome = estoque.loc[estoque['Id'] == item, 'Nome'].values[0]
                em_estoque = estoque.loc[estoque['Id'] == item, 'Quantidade'].values[0]
                preco = estoque.loc[estoque['Id'] == item, 'Preco'].values[0] 
                categoria = estoque.loc[estoque['Id'] == item, 'Categoria'].values[0]
                
                # Regra de negócio: Impede que o usuário compre 0, valores negativos ou peça mais do que há no estoque físico
                if qtd <= 0 or qtd > em_estoque:
                    print(f'Quantidade indisponível! Em estoque: {em_estoque}')
                    input('Pressione Enter para ajustar...')
                    continue

                # Cria o dicionário representando o item no carrinho. O 'Id' é guardado para a futura baixa no banco
                item_add = {
                    'Id': item,
                    'Nome': nome,
                    'Preço': preco,
                    'Quantidade': qtd,
                    'Categoria': categoria
                }

                # Adiciona o dicionário à nossa lista do carrinho de compras
                carrinho.append(item_add)
                print(f'''
                        ✔ Item adicionado com sucesso!
                        Item: {nome}   
                        Preço: R$ {preco:.2f}
                        Quantidade: {qtd}
                        ''')
                input('Pressione Enter para continuar comprando...')
                break  # Aborta o laço da quantidade e retorna para a listagem/seleção de itens

    # --------------------------------------------------
    # OPÇÃO 1: FECHAR O CARRINHO (BAIXA NO BANCO DE DADOS)
    # --------------------------------------------------
    elif pag1 == '1':
        # Proteção: Impede o fechamento de uma venda sem nenhum item adicionado
        if not carrinho:
            print("\n Seu carrinho está vazio! Adicione itens primeiro.")
            input("Pressione Enter para voltar...")
            continue
            
        limpar_tela()
        print("--- FECHAMENTO DE PEDIDO ---")
        # Converte a lista temporária de dicionários em um DataFrame para formatar a saída na tela como tabela
        carrinho_df = pd.DataFrame(carrinho)
        print(carrinho_df[['Nome', 'Preço', 'Quantidade']].to_string(index=False))
        
        # Calcula o somatório total multiplicando a série de Preço pela série de Quantidade
        total = (carrinho_df['Preço'] * carrinho_df['Quantidade']).sum()
        print(f"\nTOTAL DO PEDIDO: R$ {total:.2f}")
        print(funcoes.mostrar_linha())
        
        # LOOP DE VALIDAÇÃO: Bloqueia a execução forçando o usuário a responder estritamente '1' ou '2'
        while True:
            confirmar = input("Confirmar fechamento e atualizar estoque? (1-Sim / 2-Não): ").strip()
            if confirmar in ["1", "2"]:
                break  # Sai do laço se a resposta for aceitável
            print("Opção inválida! Digite apenas 1 para Sim ou 2 para Não.\n")
        
        # Usuário confirmou a venda?
        if confirmar == "1":
            # Abre um bloco transacional encapsulado (Garante que ou TUDO é atualizado ou NADA é alterado se houver erro)
            with engine.begin() as conexao:
                for produto in carrinho:
                    # Encontra a quantidade que está atualmente registrada na memória do Pandas
                    qtd_atual = estoque.loc[estoque['Id'] == produto['Id'], 'Quantidade'].values[0]
                    # Subtrai a quantidade que está sendo vendida
                    nova_qtd = qtd_atual - produto['Quantidade']
                    
                    # Prepara a query SQL parametrizada para evitar falhas de injeção de dados
                    sql = text("UPDATE Produtos SET Quantidade = :nova_qtd WHERE Id = :id_item")
                    # Executa a baixa do item em loop dentro da transação segura
                    conexao.execute(sql, {"nova_qtd": nova_qtd, "id_item": produto['Id']})
            
            # Sincroniza o Pandas novamente com o banco de dados atualizado pós-venda
            atualizar_estoque_memoria()
            carrinho.clear() # Esvazia a memória do carrinho para preparar o terminal para a próxima compra
            print("\n✔ Venda concluída com sucesso e estoque atualizado!")
            input("Pressione Enter para retornar ao menu...")
        else:
            print("\n Fechamento cancelado. Itens mantidos no carrinho.")
            input("Pressione Enter para retornar...")

    # --------------------------------------------------
    # OPÇÃO 2: CANCELAR O PEDIDO INTEGRALMENTE
    # --------------------------------------------------
    elif pag1 == '2':
        if not carrinho:
            print("\nO carrinho já está vazio.")
        else:
            carrinho.clear() # Limpa todos os elementos da lista, resetando o pedido atual
            print("\n❌ Pedido cancelado e carrinho limpo com sucesso!")
        input("Pressione Enter para voltar...")

    # --------------------------------------------------
    # OPÇÃO 3: REMOVER OU REDUZIR UM ITEM DO CARRINHO
    # --------------------------------------------------
    elif pag1 == '3':
        while True:
            limpar_tela()
            print("--- REMOVER / REDUZIR ITEM DO CARRINHO ---")
            
            # Validação: Se o carrinho estiver vazio, cancela a operação
            if not carrinho:
                print("\n[ Seu carrinho está vazio atualmente ]")
                print(funcoes.mostrar_linha())
                input("Pressione Enter para retornar ao menu...")
                break
            
            # Exibe o carrinho atual com a coluna de quantidade para o usuário se orientar
            carrinho_df = pd.DataFrame(carrinho)
            print(carrinho_df[['Id', 'Nome', 'Preço', 'Quantidade']].to_string(index=False))
            print(funcoes.mostrar_linha())
            
            id_remover = input('Digite o ID do item que deseja alterar ou -1 para retornar: ').strip()
            
            if id_remover == '-1':
                break
                
            try:
                id_remover = int(id_remover)
            except ValueError:
                print('ID inválido! Use apenas números.')
                input('Pressione Enter para tentar novamente...')
                continue
            
            # Busca o produto correspondente dentro da lista do carrinho
            produto_selecionado = None
            for produto in carrinho:
                if produto['Id'] == id_remover:
                    produto_selecionado = produto
                    break
            
            # Se o ID não for encontrado na lista do carrinho, alerta o usuário
            if produto_selecionado == None:
                print(f"\n❌ O ID {id_remover} não está no seu carrinho.")
                input("Pressione Enter para tentar novamente...")
                continue
            
            # Sub-loop para capturar e validar a quantidade a ser removida
            while True:
                print(f"\n-> Produto: {produto_selecionado['Nome']} (No carrinho: {produto_selecionado['Quantidade']})")
                qtd_remover = input('Quantas unidades deseja remover? (ou -1 para cancelar): ').strip()
                
                if qtd_remover == '-1':
                    break
                    
                try:
                    qtd_remover = int(qtd_remover)
                except ValueError:
                    print('Quantidade inválida! Digite um número inteiro.')
                    continue
                
                # Impede que o usuário digite números negativos ou zero para remoção
                if qtd_remover <= 0:
                    print('A quantidade a remover deve ser maior que zero!')
                    continue
                
                # Regra de negócio: Impede remover mais do que o usuário realmente tem no carrinho
                if qtd_remover > produto_selecionado['Quantidade']:
                    print(f"Erro! Você tentou remover {qtd_remover}, mas só tem {produto_selecionado['Quantidade']} no carrinho.")
                    continue
                
                # SE DESEJA REMOVER EXATAMENTE A MESMA QUANTIDADE OU MAIS: Deleta o item do carrinho
                if qtd_remover == produto_selecionado['Quantidade']:
                    carrinho.remove(produto_selecionado)
                    print(f"\n✔ '{produto_selecionado['Nome']}' foi totalmente removido do carrinho.")
                
                # SE DESEJA APENAS REDUZIR: Subtrai a quantidade do dicionário em memória
                else:
                    produto_selecionado['Quantidade'] -= qtd_remover
                    print(f"\n✔ Foram removidas {qtd_remover} unidades de '{produto_selecionado['Nome']}'.")
                    print(f"Quantidade restante no carrinho: {produto_selecionado['Quantidade']}")
                
                input("Pressione Enter para continuar...")
                break # Sai do loop da quantidade
                
            break # Sai do loop de remoção e volta ao menu principal

    # --------------------------------------------------
    # OPÇÃO 4: EXIBIR O CARRINHO ATUAL NA TELA
    # --------------------------------------------------
    elif pag1 == '4':
        limpar_tela()
        print("--- SEU CARRINHO ATUAL ---")
        if not carrinho:
            print("[ Vazio ]")
        else:
            carrinho_df = pd.DataFrame(carrinho)
            # Filtra e exibe de forma tabular apenas as colunas amigáveis ao usuário
            print(carrinho_df[['Nome', 'Preço', 'Quantidade']].to_string(index=False))
            # Calcula o valor total parcial somado até o momento
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
        break  # Corta o loop eterno 'while True', encerrando o script em definitivo
        
    # Tratamento para capturas textuais errôneas digitadas na raiz do menu principal
    else:
        print("Opção inválida!")
        input("Pressione Enter para tentar novamente...")

