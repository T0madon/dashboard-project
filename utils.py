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

# Filtro para as datas selecionadas

# Lista de dataframes e suas respectivas colunas de ano
dataframes_col_anos = [
    (artigos, 'anopubli'),
    (bolsas, 'ano'),
    (congressos, 'anoconclusao'),
    (financiados, 'anopubli'),
    (orientacoes, 'anoconclusao'),
    (produtividade, 'ano'),
    (projetos, 'anopubli')
]

# Filtros de df

    # Produção de projetos por departamento -> departamento; anopubli; quantidade_prod
dep_prod = projetos.groupby(
    ['departamento', 'anopubli']
    )['nome'].count().reset_index()
dep_prod.rename(columns={"nome": "projetos_departamento"}, inplace=True)
        # Arrumando bug do departamento
dep_prod['departamento'] = dep_prod['departamento'].str.split(',')
dep_prod = dep_prod.explode('departamento')
dep_prod = dep_prod.groupby(
    ['departamento', 'anopubli'], 
    as_index=False
    )['projetos_departamento'].sum()


    # Filtrando projeto por tipo (pesquisa, extensao, desenvolvimento, outra)
proj_tipo = projetos.groupby(
    ['departamento', 'anopubli', 'tipo']
    )['nome'].count().reset_index()
proj_tipo.rename(columns={"nome": "projetos_departamento"}, inplace=True)
        # Arrumando bug do departamento
proj_tipo['departamento'] = proj_tipo['departamento'].str.split(',')
proj_tipo = proj_tipo.explode('departamento')
proj_tipo = proj_tipo.groupby(
    ['departamento', 'anopubli', 'tipo'], 
    as_index=False
    )['projetos_departamento'].sum()


    # SETORES
setores = professores[
            ['setor', 'departamento']
        ].drop_duplicates().sort_values(by=['setor', 'departamento'])