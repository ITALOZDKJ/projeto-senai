 ☕ Cafeteria Virtual
Visão Geral do Projeto
O objetivo deste projeto é desenvolver um sistema simples de cafeteria virtual utilizando Python, SQLite e Pandas. O sistema funciona via terminal (CLI) e permite realizar o gerenciamento de pedidos, produtos e comandas de forma interativa.
O projeto foi estruturado para simular o funcionamento básico de uma cafeteria, permitindo:
Cadastro e armazenamento de produtos em banco SQLite.
Exibição de cardápio.
Criação de comandas.
Controle de pedidos.
Registro de horário e data das vendas.
Manipulação e visualização de dados utilizando Pandas.

Estrutura de Dados
Tabela: produtos
Responsável por armazenar os itens disponíveis no cardápio.
Campo
Tipo
Descrição
Codigo
INTEGER
Identificador único do produto
nome
TEXT
Nome do produto
preco
REAL
Valor unitário do produto

Produtos cadastrados atualmente
Café
Chá de camomila
Chocolate

Tabela: comanda
Responsável por armazenar os pedidos realizados.
Campo
Tipo
Descrição
id
INTEGER
Identificador do pedido
Nome
TEXT
Nome do produto
Quantidade
INTEGER
Quantidade solicitada
Valor_Unitario
REAL
Valor unitário do produto
Valor_Total
REAL
Valor total do item
Codigo
INTEGER
Código da comanda
Data
TEXT
Data do pedido
Hora
TEXT
Hora do pedido


Requisitos Funcionais
RF01 - Cadastro de Produtos
O sistema deve permitir o cadastro de produtos no banco de dados SQLite.
RF02 - Exibição do Cardápio
O sistema deve listar todos os produtos disponíveis com seus respectivos preços.
RF03 - Criação de Comandas
O sistema deve gerar uma nova comanda para cada atendimento realizado.
RF04 - Adição de Pedidos
O usuário deve conseguir adicionar produtos à comanda informando o item desejado.
RF05 - Remoção de Itens
O sistema deve permitir remover o último item inserido na comanda.
RF06 - Controle de Quantidade
Ao repetir um item já existente na comanda, o sistema deve atualizar a quantidade automaticamente.
RF07 - Cálculo Automático
O sistema deve calcular automaticamente:
Valor unitário
Quantidade
Valor total da compra
RF08 - Registro de Data e Hora
O sistema deve registrar automaticamente a data e o horário da venda utilizando o fuso horário de São Paulo.
RF09 - Persistência de Dados
As informações devem permanecer armazenadas no banco SQLite mesmo após o encerramento do programa.

Requisitos Não Funcionais
RNF01 - Interface
A interação do usuário ocorre inteiramente pelo terminal.
RNF02 - Banco de Dados
Os dados são armazenados utilizando SQLite.
RNF03 - Manipulação de Dados
A biblioteca Pandas é utilizada para leitura e exibição dos dados.
RNF04 - Linguagem
O projeto foi desenvolvido em Python.

Regras de Negócio
RN01
O sistema não deve permitir produtos duplicados na tabela produtos.
RN02
Toda nova comanda deve possuir um código único.
RN03
Ao remover um item da comanda:
Caso a quantidade seja maior que 1, apenas uma unidade deve ser removida.
Caso a quantidade seja igual a 1, o item deve ser removido completamente.
RN04
Os valores totais devem ser recalculados automaticamente após qualquer alteração na comanda.

Tecnologias Utilizadas
Python
SQLite3
Pandas
Datetime
ZoneInfo

Estrutura Atual do Projeto
cafeteria_virtual/
│
├── cafeteria.db
├── cafeteria_virtual.ipynb
├── README.md
│
└── scripts auxiliares
    ├── criação de tabelas
    ├── inserção de produtos
    ├── limpeza de tabelas
    └── consultas


Autor
Projeto desenvolvido por Ítalo Lopes como prática de desenvolvimento em Python, banco de dados SQLite e manipulação de dados com Pandas.

