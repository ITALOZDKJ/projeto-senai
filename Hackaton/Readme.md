# 🛠 Ferragens do Zé - Controle de Estoque & Frente de Caixa

## Visão Geral do Projeto
O objetivo deste projeto é desenvolver um sistema robusto e interativo para o gerenciamento de estoque e frente de caixa (PDV) da loja **Ferragens do Zé**, utilizando Python, SQLAlchemy, PyMySQL e Pandas. 

O sistema funciona inteiramente via terminal (CLI), conectando-se a um banco de dados relacional MySQL hospedado em rede local, permitindo o gerenciamento dinâmico de mercadorias e a simulação de vendas operadas em tempo real.

O projeto foi estruturado para resolver os seguintes problemas práticos:
* Conexão e persistência relacional com banco de dados MySQL via SQLAlchemy.
* Controle rigoroso de estoque com proteção contra saldos negativos.
* Cadastro interativo de novos produtos com telas de confirmação de dados.
* Fluxo completo de Frente de Caixa com carrinho de compras virtual.
* Possibilidade de edição (adição/remoção/redução) de itens antes de fechar a comanda.
* Sincronização em tempo real entre a memória da aplicação (DataFrames Pandas) e o banco físico.

---

## Estrutura de Dados

### Tabela: `Produtos`
Responsável por armazenar as mercadorias comercializadas no estabelecimento.

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **Id** | `INTEGER (PK)` | Identificador único e autoincremental do produto |
| **Nome** | `VARCHAR/TEXT` | Nome ou descrição do item de ferragem |
| **Preco** | `DECIMAL/FLOAT`| Valor unitário de venda da mercadoria |
| **Categoria**| `VARCHAR/TEXT` | Grupo ao qual o item pertence (Ex: Ferramentas, Elétrica) |
| **Quantidade**| `INTEGER` | Saldo físico atual disponível em estoque |

---

## Requisitos Funcionais

* **RF01 - Sincronização em Memória (Pandas):** O sistema deve carregar e atualizar constantemente DataFrames do Pandas para agilizar consultas locais e validações de dados.
* **RF02 - Adição de Saldo ao Estoque:** O usuário deve ser capaz de selecionar um ID válido e dar entrada de novas unidades a um produto já existente.
* **RF03 - Remoção Manual de Estoque:** O sistema deve permitir dar baixa manual em unidades de estoque (ex: descarte por avaria).
* **RF04 - Cadastro de Novos Itens:** O sistema deve permitir criar novos produtos coletando Nome, Preço, Categoria (com base nas já existentes) e Quantidade inicial.
* **RF05 - Tela de Confirmação de Cadastro:** Antes de persistir um novo produto no MySQL, o sistema deve apresentar um sumário dos dados para aprovação do usuário.
* **RF06 - Frente de Caixa (Carrinho):** O terminal deve possuir um módulo de PDV onde itens são adicionados dinamicamente a uma lista temporária.
* **RF07 - Alteração Dinâmica do Carrinho:** No módulo de caixa, o operador deve conseguir remover completamente um item ou reduzir unidades parciais (ex: mudar de 6 para 5 unidades no carrinho).
* **RF08 - Fechamento de Venda Transacional:** O fechamento do carrinho deve abater automaticamente as quantidades do banco de dados MySQL de forma segura.
* **RF09 - Cálculo de Parciais e Totais:** Tanto na exibição do carrinho quanto no fechamento, o Pandas deve calcular automaticamente os somatórios com base no `Preço × Quantidade`.

---

## Requisitos Não Funcionais

* **RNF01 - Interface:** A interface com o usuário ocorre estritamente via Prompt de Comando (CLI), com rotinas automáticas de limpeza de tela (`cls` / `clear`) para focar a atenção do operador.
* **RNF02 - Banco de Dados Relacional:** O armazenamento definitivo dos dados é realizado utilizando um servidor MySQL.
* **RNF03 - Driver e ORM:** A comunicação com o servidor MySQL é feita através do driver `PyMySQL` gerenciado pela biblioteca `SQLAlchemy`.
* **RNF04 - Manipulação de Dados:** O `Pandas` é a ferramenta central para renderização tabular das tabelas de estoque e do carrinho de compras.
* **RNF05 - Linguagem de Programação:** Todo o ecossistema do software foi construído em Python 3.

---

## Regras de Negócio

* **RN01 - Prevenção de Estoque Negativo:** O sistema jamais deve permitir que uma venda ou remoção manual deixe o saldo do produto na tabela `Produtos` menor que zero.
* **RN02 - Validação de Entradas Numéricas:** Toda entrada de dados via teclado que exija números (IDs, Quantidades, Preços) deve ser blindada contra erros de digitação (`ValueError`), impedindo a quebra do programa.
* **RN03 - Valores Maiores que Zero:** Quantidades inseridas para compra ou reabastecimento devem ser obrigatoriamente inteiros maiores que zero.
* **RN04 - Segurança de Transação (Atomizacão):** O fechamento do carrinho de compras deve rodar dentro de um bloco transacional (`engine.begin()`). Se um único item falhar ao atualizar, nenhuma alteração deve ser gravada (Garantia de integridade).
* **RN05 - Ajuste de Formatação de Moeda:** No cadastro de novos itens, o sistema deve aceitar números com vírgula e convertê-los automaticamente para ponto antes de enviar ao banco de dados.

---

## Tecnologias Utilizadas

* **Python**
* **SQLAlchemy**
* **PyMySQL**
* **Pandas**
* **OS** *(Módulo nativo para comandos de terminal)*

---

## Estrutura Atual do Projeto

```text
ferragens_do_ze/
│
├── funcoes.py                # Módulo auxiliar com configurações de conexões e estética
├── controle_estoque.py       # Script principal do Módulo de Estoque (Opções 1, 2, 3 e 4)
├── frente_de_caixa.py        # Script principal do Módulo de PDV/Carrinho
└── README.md                 # Documentação do projeto