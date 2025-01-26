# from fastapi import FastAPI
# import psycopg2
# import pandas as pd

# app = FastAPI()

# # Conexão com o banco de dados
# def get_data():
#     conn = psycopg2.connect(
#         host="SEU_HOST",
#         database="SEU_DATABASE",
#         user="SEU_USUARIO",
#         password="SUA_SENHA"
#     )
#     query = "SELECT * FROM tabela_exemplo;"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# @app.get("/dados")
# def dados():
#     df = get_data()
#     return df.to_dict(orient="records")