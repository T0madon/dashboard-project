from pathlib import Path
import psycopg2
import plotly.express as px
import pandas as pd

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

def writeDf(df_name, table):
    # print(f'\n{df_name}\n')
    datas, columns = buscar_dados(f"SELECT * FROM {table}")
    df = pd.DataFrame(datas, columns=columns)
    df.to_csv(PATH_SAVE_DF / f"{df_name}.csv", decimal=",", sep=";")
    

# Buscar dados
# print('INÍCIO\n')
# writeDf('df_artigos', 'artigos')
# writeDf('df_bolsas', 'bolsas')
# writeDf('df_congressos', 'congressos')
# writeDf('df_financiados', 'financiados')
# writeDf('df_orientacoes', 'orientacoes')
# writeDf('df_produtividade', 'produtividade')
# writeDf('df_professores', 'professores')
# writeDf('df_projetos', 'projetos')


# teacher_data, teacher_columns = buscar_dados("SELECT * FROM professores")
# teachers_df = pd.DataFrame(teacher_data, columns=teacher_columns)
# print(teachers_df)


print('\nPROJETOS\n')
project_data, project_columns = buscar_dados("SELECT * FROM projetos")
projects_df = pd.DataFrame(project_data, columns=project_columns)
teste = pd.read_csv(PATH_SAVE_DF / 'df_projetos.csv', sep=';', decimal=',', index_col=0)

print(projects_df)
print('-' * 50)
print(teste)

# print('PRODUÇÃO POR DEPARTAMENTO\n')
# dep_prod_df = projects_df.groupby(['departamento', 'anopubli'])['nome'].count().reset_index()
# dep_prod_df.rename(columns={"nome": "quantidade_produ"}, inplace=True)
# print(dep_prod_df)



# id_teacher = '6f3420dc-4281-4019-b672-5e3f13caec88'

# df1 = teachers_df[teachers_df['id_professor'] == id_teacher]
# df2 = projects_df[projects_df['id_professor'] == id_teacher]

# print(df1['nome'])

# res = pd.concat([df1, df2], ignore_index=True)
# print(f'COLUNAS: {res.columns}')
# print(res)

# for index, professor in enumerate(dados):
#     print(f'BUSCA {index + 1}')
#     for i, valor in enumerate(professor):
#         print(f'{colunas[i]} = {valor}')
#     print('-' * 40)