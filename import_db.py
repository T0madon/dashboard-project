from pathlib import Path
import psycopg2
import pandas as pd
import os

ROOT = Path(__file__).parent
PATH_SAVE_DF = ROOT / 'dataframes' 

# Conectar ao banco de dados
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="banco2",
            user="postgres",
            password="Gumattos2",
            host="localhost",  
            port="5432"        
        )
        print("Conexão bem-sucedida!")
        cursor = conn.cursor()
        os.makedirs('dataframes', exist_ok=True)

        # Busca todas as tabelas do schema 'public'
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        tables = cursor.fetchall()

        for table_name, in tables:
            df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn) # type: ignore
            df.to_csv(PATH_SAVE_DF / f'df_{table_name}.csv', 
                    #   index=False, 
                    #   encoding='utf-8-sig',
                      sep=';')
            print(f'Tabela {table_name} salva como df_{table_name}.csv')


        # Fecha a conexão
        cursor.close()
        conn.close()


    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

# Testar conexão
conexao = conectar_banco()
if conexao:
    conexao.close()

conectar_banco()


# def buscar_dados(query):
#     conn = conectar_banco()
#     if not conn:
#         return []
    
#     try:
#         cur = conn.cursor()
#         cur.execute(query)
#         dados = cur.fetchall()
#         colunas = [desc[0] for desc in cur.description]  # Nome das colunas
#         cur.close()
#         conn.close()
#         return dados, colunas
#     except Exception as e:
#         print("Erro ao buscar dados:", e)
#         return []

# def writeDf(df_name, table):
#     # print(f'\n{df_name}\n')
#     datas, columns = buscar_dados(f"SELECT * FROM {table}")
#     df = pd.DataFrame(datas, columns=columns)
#     df.to_csv(PATH_SAVE_DF / f"{df_name}.csv", sep=";")
    
# writeDf('df_artigos', 'artigos')
# writeDf('df_bolsas', 'bolsas')
# writeDf('df_congressos', 'congressos')
# writeDf('df_financiados', 'financiados')
# writeDf('df_orientacoes', 'orientacoes')
# writeDf('df_produtividade', 'produtividade')
# writeDf('df_professores', 'professores')
# writeDf('df_projetos', 'projetos')