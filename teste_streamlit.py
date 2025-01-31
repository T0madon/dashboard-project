import streamlit as st
import pandas as pd
from graphs import dep_prod_graph

# CONSTRUÇÃO DO DASHBOARD

st.set_page_config(layout='wide')
st.title("Produções Científicas UEPG")

aba1, aba2 = st.tabs(['Departamentos', 'Professores'])

with aba1:
    # Insights

    # Gráfico
    with st.container(border=True):
        st.plotly_chart(dep_prod_graph, use_container_width=False)
    