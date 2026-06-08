import pymysql
import pandas as pd

from sqlalchemy import create_engine
from datetime import datetime
from zoneinfo import ZoneInfo
engine = create_engine(
    "mysql+pymysql://admin:senaiead@172.16.22.76/cafeteria"
)


# ==========================================
# 1. CRIAÇÃO DAS TABELAS (Ajustado para MySQL)
# ==========================================
import pymysql.cursors


def obter_conexao():
    return pymysql.connect(
        host="172.16.22.76",
        user="admin",
        password="senaiead",
        database="cafeteria",
        # Retorna os resultados em formato de dicionário, facilitando consultas
        cursorclass=pymysql.cursors.DictCursor,
    )
con = obter_conexao()
cur = con.cursor()
con = obter_conexao()
with con.cursor() as cur:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Produtos (
            Codigo INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            preco DECIMAL(10,2) NOT NULL,
            UNIQUE(nome)
        )
    """
    )

    

    # No MySQL, a chave estrangeira (FOREIGN KEY) precisa ser declarada explicitamente
    cur.execute(
        """
       CREATE TABLE IF NOT EXISTS ComandaCliente (
    Codigo_da_comanda INT PRIMARY KEY,
    Valor DECIMAL(10,2) NOT NULL,
    Data VARCHAR(20) NOT NULL,
    Hora VARCHAR(20) NOT NULL
);
        
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS Comanda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Quantidade INT NOT NULL,
    Valor_Unitario DECIMAL(10,2) NOT NULL,

    Codigo_Pedido INT NOT NULL,

    CONSTRAINT fk_comanda
        FOREIGN KEY (Codigo_Pedido)
        REFERENCES ComandaCliente(CodigoComanda)
        ON DELETE CASCADE
        );
    """
    )
con.commit()
con.close()


# ==========================================
# 2. POPULAR PRODUTOS (Ignora se já existirem)
# ==========================================
con = obter_conexao()
with con.cursor() as cur:
    # INSERT IGNORE evita erros caso você rode o script mais de uma vez
    cur.execute(
        """
    INSERT IGNORE INTO Produtos (nome, preco) VALUES
    ('Café', 5.00),
    ('Chá de camomila', 6.00),
    ('Chocolate', 8.00)
    """
    )




con.commit()
con.close()
cardapio = pd.read_sql_query(
    "SELECT * FROM Produtos",
    engine
)
print(cardapio)