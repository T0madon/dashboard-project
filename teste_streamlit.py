from pathlib import Path
import streamlit as st
import pandas as pd

ROOT = Path(__file__).parent
PATH_SAVE_DF = ROOT / 'dataframes' 
TABELAS = [
    'artigos', 'bolsas', 'congressos', 'financiados',
    'orientacoes', 'produtividade', 'professores', 'projetos'
]

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

# Filtrando os df de acordo com as necessidades do dashboard

    # Produção por departamento -> departamento; anopubli; quantidade_prod
dep_prod = projetos.groupby(['departamento', 'anopubli'])['nome'].count().reset_index()
dep_prod.rename(columns={"nome": "quantidade_prod"}, inplace=True)


# CONSTRUÇÃO DO DASHBOARD
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
opcoes = {
    "Artigos": artigos,
    "Bolsas": bolsas,
    "Congressos": congressos,
    "Financiados": financiados,
    "Orientações": orientacoes,
    "Produtividade": produtividade,
    "Professores": professores,
    "Projetos": projetos
}

# SideBar
select_df = st.sidebar.selectbox("Selecione a tabela: ", list(opcoes.keys()))
df_selected = opcoes[select_df]
    # Colunas
col1, col2 = st.sidebar.columns(2)
col_filtro = col1.multiselect("Selecione as colunas", 
               [c for c in df_selected if c not in["id_professor"]])
# valor_filtro = col2.selectbox("Selecione o valor",
#                list(value for value in ))

    # Buttons
st_filtrar = col1.button("Filtrar")
st_limpar = col2.button("Limpar")

    # Send
if st_filtrar:
    st.dataframe(df_selected[col_filtro])
