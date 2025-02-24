import streamlit as st
from graphs import dep_prod_graph
from utils import (artigos, bolsas, congressos, financiados, orientacoes,
                   produtividade, professores, projetos, setores)
# CONSTRUÇÃO DO DASHBOARD

st.set_page_config(layout='wide')
st.title("Produções Científicas UEPG")

st.sidebar.title('Filtros')

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

    # Gráfico
    with st.container(border=True):
        st.plotly_chart(dep_prod_graph, use_container_width=False)
    