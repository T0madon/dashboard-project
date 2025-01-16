import psycopg2
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Conectar ao banco de dados
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="banco2",
            user="postgres",
            password="Gumattos2",
            host="localhost",  # ou IP do servidor do banco
            port="5432"        # porta padrão do PostgreSQL
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Testar conexão
conexao = conectar_banco()
if conexao:
    conexao.close()

def buscar_dados(query):
    conn = conectar_banco()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute(query)
        dados = cur.fetchall()
        colunas = [desc[0] for desc in cur.description]  # Nome das colunas
        cur.close()
        conn.close()
        return dados, colunas
    except Exception as e:
        print("Erro ao buscar dados:", e)
        return []

# Buscar dados

dados, colunas = buscar_dados("SELECT * FROM professores LIMIT 100")
print('INÍCIO\n')
# print(dados[0][1])

for index, professor in enumerate(dados):
    print(f'BUSCA {index + 1}')
    for i, valor in enumerate(professor):
        print(f'{colunas[i]} = {valor}')
    print('-' * 40)