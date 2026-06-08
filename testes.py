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

teste = 5

comanda = pd.read_sql_query("""
                                
                                SELECT * FROM 
                                
                                """)        