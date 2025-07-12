import streamlit as st
from io import BytesIO

from utils import (artigos, bolsas, congressos, financiados, orientacoes, 
                   produtividade, professores, projetos)

st.set_page_config(page_title="Visualização dos DataFrames", layout="wide")

# Função auxiliar para corrigir colunas com múltiplos departamentos
def corrigir_departamentos(df, coluna='departamento'):
    df[coluna] = df[coluna].str.split(',')
    df = df.explode(coluna)
    df[coluna] = df[coluna].str.strip()
    return df

# Função auxiliar para download de CSV
def gerar_csv_download(df, nome_arquivo):
    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name=f"{nome_arquivo}.csv",
        mime='text/csv'
    )

# Lista de dataframes com seus nomes e tratamento necessário
dataframes_info = [
    ("Artigos", artigos),
    ("Bolsas", bolsas),
    ("Congressos", congressos),
    ("Financiados", financiados),
    ("Orientações", orientacoes),
    ("Produtividade", produtividade),
    ("Professores", professores),
    ("Projetos", projetos),
]

st.title("📚 Visualização dos DataFrames")

for nome, df in dataframes_info:
    st.subheader(f"📌 {nome}")
    
    # Corrigir departamentos se a coluna existir
    if 'departamento' in df.columns:
        df = corrigir_departamentos(df.copy())
    
    # Filtro de colunas
    colunas_disponiveis = df.columns.tolist()
    colunas_selecionadas = st.multiselect(
        f"Selecione as colunas que deseja visualizar em '{nome}':",
        options=colunas_disponiveis,
        default=colunas_disponiveis
    )
    
    # Visualização
    df_filtrado = df[colunas_selecionadas]
    st.dataframe(df_filtrado, use_container_width=True)

    # Campo para nome do arquivo e botão de download
    nome_arquivo = st.text_input(f"Digite o nome do arquivo para download ({nome}):", value=f"{nome.lower()}")
    gerar_csv_download(df_filtrado, nome_arquivo)

    st.markdown("---")

