import streamlit as st
import plotly.express as px
from graphs import dep_prod_graph
from utils import (artigos, bolsas, congressos, financiados, orientacoes,
                   produtividade, professores, projetos, setores, dep_prod)
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
        setores['setor'].unique().tolist()
        )
    
# Filtrando os departamentos de acordo com o setor escolhido
df_departamentos_filtrados = setores[setores['setor'].isin(setores_selecionados)]
    
#SIDEBAR - Departamentos
with st.sidebar.expander('Departamentos'):
    departamentos_selecionados = st.multiselect(
        'Selecione o(s) departamento(s)',
        df_departamentos_filtrados['departamento'].unique().tolist()
        )
    
aba1, aba2 = st.tabs(['Departamentos', 'Professores'])

with aba1:
    # Insights

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
                title='Produção por Departamento'
            )
            # dep_prod_graph.update_traces(visible="legendonly")
            st.plotly_chart(dep_prod_graph, use_container_width=False)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")
    