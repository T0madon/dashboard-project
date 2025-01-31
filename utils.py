import pandas as pd
from pathlib import Path

# Caminhos e dados
ROOT = Path(__file__).parent
PATH_SAVE_DF = ROOT / 'dataframes' 
TABELAS = [
    'artigos', 'bolsas', 'congressos', 'financiados',
    'orientacoes', 'produtividade', 'professores', 'projetos'
]

# Funções
    # Função para ler os arquivos CSV de acordo com o nome da tabela no db
def read_csv(table):
    return pd.read_csv(PATH_SAVE_DF / f'df_{table}.csv', sep=';', index_col=0)

# Criando todos os dataframes(df) necessários para todas as tabelas
artigos = read_csv('artigos')
bolsas = read_csv('bolsas')
congressos = read_csv('congressos')
financiados = read_csv('financiados')
orientacoes = read_csv('orientacoes')
produtividade = read_csv('produtividade')
professores = read_csv('professores')
projetos = read_csv('projetos')

# Filtros de df

    # Produção por departamento -> departamento; anopubli; quantidade_prod
dep_prod = projetos.groupby(['departamento', 'anopubli'])['nome'].count().reset_index()
dep_prod.rename(columns={"nome": "quantidade_prod"}, inplace=True)
        # Arrumando bug do departamento
dep_prod['departamento'] = dep_prod['departamento'].str.split(',')
dep_prod = dep_prod.explode('departamento')
dep_prod = dep_prod.groupby(['departamento', 'anopubli'], as_index=False)['quantidade_prod'].sum()


dep_prod.to_csv(PATH_SAVE_DF / f"dep_prod.csv", sep=";")