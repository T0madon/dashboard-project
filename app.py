import streamlit as st
import plotly.express as px
from graphs import dep_prod_graph
from utils import (setores, dep_prod, projetos)

# CONSTRUÇÃO DO DASHBOARD

st.set_page_config(layout='wide')
st.title("Produções Científicas UEPG")

st.sidebar.title('Filtros')

# SIDEBAR - Variáveis
# with st.sidebar.expander('Variáveis'):
#     vars = st.multiselect(
#         'Selecione a(s) variável(is)',
#     )

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
    
aba1, aba2 = st.tabs(['Departamentos', 'Professores'])

with aba1:
    coluna1, coluna2, coluna3 = st.columns(3)

    # Seleciona os projetos dos departamentos selecionados
    projetos_filtrados = projetos[projetos['departamento'].isin(departamentos_selecionados)]

    with coluna1:
        
        # Contar o número total de projetos filtrados
        total_projetos = projetos_filtrados.shape[0]
        
        st.metric('Total de projetos dos departamentos selecionados', value=total_projetos)

    with coluna2:
        ...

    # Filtrar o dataframe do gráfico pelos departamentos selecionados
    dep_prod_filtrado = dep_prod[dep_prod['departamento'].isin(departamentos_selecionados)]

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
                line_dash='departamento',
                title='Produção Total Por Departamento'
            )
            # dep_prod_graph.update_traces(visible="legendonly") #Vem marcado tudo no gráfico
            st.plotly_chart(dep_prod_graph, use_container_width=False)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")