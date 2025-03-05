import streamlit as st
import plotly.express as px
from graphs import dep_prod_graph
from utils import (artigos, bolsas, congressos, financiados, orientacoes, 
                   produtividade, professores, projetos, setores, dep_prod, 
                   dataframes_col_anos)

# CONSTRUÇÃO DO DASHBOARD

st.set_page_config(layout='wide')
st.title("Produções Científicas UEPG")
st.sidebar.title('Filtros')

# SIDEBAR - Setores
with st.sidebar.expander('Setores'):
    setores_selecionados = st.multiselect(
        'Selecione o(s) setor(es)',
        setores['setor'].unique().tolist(),
        default=['SEXATAS'] if 'SEXATAS' in setores['setor'].unique() else [] 
        )  
# Filtrando os departamentos de acordo com o setor escolhido
df_departamentos_filtrados = setores[setores['setor'].isin(setores_selecionados)]
    
#SIDEBAR - Departamentos
with st.sidebar.expander('Departamentos'):
    departamentos_selecionados = st.multiselect(
        'Selecione o(s) departamento(s)',
        df_departamentos_filtrados['departamento'].unique().tolist(),
        default=df_departamentos_filtrados['departamento'].unique().tolist()
        )
# Filtrar o dataframe do gráfico pelos departamentos selecionados
dep_prod_filtrado = dep_prod[
    dep_prod['departamento'].isin(departamentos_selecionados)
]
    
#SIDEBAR - Filtro por data
# Filtrar os dataframes pelos departamentos selecionados e extrair os anos
anos_disponiveis = []

for df, coluna_ano in dataframes_col_anos:
    df_filtrado = df[df['departamento'].isin(departamentos_selecionados)]
    # Converte para inteiro e remove NaN
    anos_validos = df_filtrado[coluna_ano].dropna().astype(int).tolist() 
    anos_disponiveis.extend(anos_validos)

# Definir o menor e o maior ano disponíveis
if anos_disponiveis:
    ano_min = min(anos_disponiveis)
    ano_max = max(anos_disponiveis)
else:
    ano_min, ano_max = 2000, 2023  # Valores padrão caso não haja dados

# SIDEBAR - Filtro de Anos
with st.sidebar.expander('Período de Análise'):
    anos_selecionados = st.slider(
        "Selecione o intervalo de anos:",
        ano_min, ano_max, (ano_min, ano_max)
    )

aba1, aba2, aba3, aba4, aba5 = st.tabs(
    ['Publicações', 'Orientações', 'Projetos', 'Titulação', 'Quantitativos']
    )

with aba3:
    coluna1, coluna2, coluna3 = st.columns(3)

    total_projetos_selecionados = dep_prod_filtrado[
        'projetos_departamento'].sum()
    
    total_projetos_geral = dep_prod[
        'projetos_departamento'
    ].sum()

    with coluna1:
        st.metric(
            'Total de projetos dos departamentos selecionados', 
            value=total_projetos_selecionados
        )

    with coluna2:
        st.write('')

    with coluna3:
        st.metric(
            'Total de projetos da UEPG',
            value=total_projetos_geral
        )

    # Gráfico
    with st.container(border=True):
        # Só cria o gráfico se houver departamentos selecionados
        if not dep_prod_filtrado.empty:
            dep_prod_graph = px.line(
                dep_prod_filtrado,
                x='anopubli',
                y='projetos_departamento',
                color='departamento',
                range_y=(0, dep_prod['projetos_departamento'].max()),
                range_x=anos_selecionados,
                line_dash='departamento',
                title='Produção Total Por Departamento'
            )
            # dep_prod_graph.update_traces(visible="legendonly") #Vem marcado tudo no gráfico
            st.plotly_chart(dep_prod_graph, use_container_width=False)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    coluna4, coluna5 = st.columns(2)

    with coluna4:
        st.warning('teste')

    with coluna5:
        st.warning('teste')
