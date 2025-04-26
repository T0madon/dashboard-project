import streamlit as st
import pandas as pd
import ast
import plotly.express as px
from graphs import dep_prod_graph

# Importação de dataframes/df filtrados
from utils import (artigos, bolsas, congressos, financiados, orientacoes, 
                   produtividade, professores, projetos, setores, dep_prod, 
                   dataframes_col_anos, proj_tipo)

# Importação de funções auxiliares
from utils import (contem_departamento)

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

#SIDEBAR
#Filtro de Anos
with st.sidebar.expander('Período de Análise'):
    anos_selecionados = st.slider(
        "Selecione o intervalo de anos:",
        ano_min, ano_max, (ano_min, ano_max)
    )

aba1, aba2, aba3, aba4, aba5 = st.tabs(
    ['Publicações', 'Orientações', 'Projetos', 'Titulação', 'Quantitativos']
    )

with aba1:
    st.header('Totais da UEPG (sem filtro)')
    # Linha 1: Métricas de artigos e resumos (sem filtros)
    col1, col2, col3 = st.columns(3)

    with col1:
        total_artigos_nacionais = len(artigos[artigos['tipo'] == 'NACIONAL'])
        st.metric("Artigos Nacionais (UEPG)", total_artigos_nacionais)

    with col2:
        total_artigos_internacionais = len(artigos[artigos['tipo'] == 'INTERNACIONAL'])
        st.metric("Artigos Internacionais (UEPG)", total_artigos_internacionais)

    with col3:
        total_resumos = len(congressos[congressos['tipo'] == 'RESUMO'])
        st.metric("Resumos em Congressos (UEPG)", total_resumos)

    # Linha 2: Métricas de resumos expandidos, completos e produtividade (sem filtros)
    col4, col5, col6 = st.columns(3)

    with col4:
        total_resumos_expandidos = len(congressos[congressos['tipo'] == 'RESUMO_EXPANDIDO'])
        st.metric("Resumos Expandidos (UEPG)", total_resumos_expandidos)

    with col5:
        total_completos = len(congressos[congressos['tipo'] == 'COMPLETO'])
        st.metric("Publicações Completas (UEPG)", total_completos)

    with col6:
        total_produtividade = len(produtividade)
        st.metric("Professores com Bolsa Produtividade", total_produtividade)

    st.header("Totais dos filtros selecionados")

    # Filtros para artigos
    artigos_filtrados = artigos[
        artigos['departamento'].apply(lambda x: contem_departamento(x, departamentos_selecionados)) &
        artigos['anopubli'].between(anos_selecionados[0], anos_selecionados[1])
    ]

    # Filtros para congressos
    congressos_filtrados = congressos[
        congressos['departamento'].apply(lambda x: contem_departamento(x, departamentos_selecionados)) &
        congressos['anoconclusao'].between(anos_selecionados[0], anos_selecionados[1])
    ]

    # Filtros para produtividade (não tem ano, só filtro por departamento)
    produtividade_filtrada = produtividade[
        produtividade['departamento'].apply(lambda x: contem_departamento(x, departamentos_selecionados)) &
        produtividade['ano'].between(anos_selecionados[0], anos_selecionados[1])
    ]

    # Linha 1 com filtros aplicados
    col1, col2, col3 = st.columns(3)

    with col1:
        total_artigos_nacionais_filtros = len(artigos_filtrados[artigos_filtrados['tipo'] == 'NACIONAL'])
        st.metric("Artigos Nacionais (filtrados)", total_artigos_nacionais_filtros)

    with col2:
        total_artigos_internacionais_filtros = len(artigos_filtrados[artigos_filtrados['tipo'] == 'INTERNACIONAL'])
        st.metric("Artigos Internacionais (filtrados)", total_artigos_internacionais_filtros)

    with col3:
        total_resumos_filtros = len(congressos_filtrados[congressos_filtrados['tipo'] == 'RESUMO'])
        st.metric("Resumos em Congressos (filtrados)", total_resumos_filtros)

    # Linha 2 com filtros aplicados
    col4, col5, col6 = st.columns(3)

    with col4:
        total_resumos_expandidos_filtros = len(congressos_filtrados[congressos_filtrados['tipo'] == 'RESUMO_EXPANDIDO'])
        st.metric("Resumos Expandidos (filtrados)", total_resumos_expandidos_filtros)

    with col5:
        total_completos_filtros = len(congressos_filtrados[congressos_filtrados['tipo'] == 'COMPLETO'])
        st.metric("Publicações Completas (filtrados)", total_completos_filtros)

    with col6:
        total_produtividade_filtros = len(produtividade_filtrada)
        st.metric("Bolsa Produtividade (filtrados)", total_produtividade_filtros)

    st.header("Totais de Artigos")

    col1, col2 = st.columns(2)

    # Pré-processa os dados de artigos (aplica filtros e trata departamentos múltiplos)
    artigos_expandido = artigos.copy()
    artigos_expandido = artigos_expandido[artigos_expandido['anopubli'].between(anos_selecionados[0], anos_selecionados[1])]

    # Expande os departamentos (uma linha para cada departamento se houver mais de um)
    artigos_expandido['departamento'] = artigos_expandido['departamento'].str.split(',')
    artigos_expandido = artigos_expandido.explode('departamento')
    artigos_expandido['departamento'] = artigos_expandido['departamento'].str.strip()

    # Filtra pelos departamentos selecionados
    artigos_expandido = artigos_expandido[artigos_expandido['departamento'].isin(departamentos_selecionados)]

    # Junta com o df de setores para ter o setor de cada departamento
    artigos_com_setores = artigos_expandido.merge(setores, on='departamento', how='left')

    # GRÁFICO POR SETOR
    df_setores = artigos_com_setores.groupby(['setor', 'anopubli']).size().reset_index(name='quantidade')
    fig_setores = px.line(
        df_setores,
        x='anopubli',
        y='quantidade',
        color='setor',
        markers=True,
        title="Artigos por Setor (por ano)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_setores.update_layout(showlegend=False)
    col1.plotly_chart(fig_setores, use_container_width=True)

    # GRÁFICO POR DEPARTAMENTO
    df_departamentos = artigos_expandido.groupby(['departamento', 'anopubli']).size().reset_index(name='quantidade')
    fig_departamentos = px.line(
        df_departamentos,
        x='anopubli',
        y='quantidade',
        color='departamento',
        markers=True,
        title="Artigos por Departamento (por ano)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_departamentos.update_layout(showlegend=False)
    col2.plotly_chart(fig_departamentos, use_container_width=True)

    st.header("Artigos Nacionais")

    # Filtro de artigos nacionais
    artigos_nacionais_filtrados = artigos[
        (artigos['tipo'] == 'NACIONAL') &
        (artigos['anopubli'].astype(int).between(anos_selecionados[0], anos_selecionados[1])) &
        (artigos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)))
    ]

    # Criando coluna de setor
    artigos_nacionais_setores = artigos_nacionais_filtrados.copy()
    artigos_nacionais_setores['setor'] = artigos_nacionais_setores['departamento'].apply(
        lambda dptos: next(
            (row['setor'] for row in setores.to_dict('records') if any(depto in dptos for depto in [row['departamento']])),
            None
        )
    )

    col1, col2 = st.columns(2)

    # Gráfico de pizza por setor
    with col1:
        setor_counts = artigos_nacionais_setores['setor'].value_counts().reset_index()
        setor_counts.columns = ['setor', 'quantidade']
        fig_pizza_setor = px.pie(
            setor_counts,
            names='setor',
            values='quantidade',
            title='Artigos Nacionais por Setor',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza_setor.update_layout(showlegend=False)
        st.plotly_chart(fig_pizza_setor, use_container_width=True)

    # Gráfico de barra por departamento
    with col2:
        # Criar uma lista para contar corretamente artigos por departamento (considerando múltiplos por linha)
        artigos_dep_expandido = []
        for _, row in artigos_nacionais_filtrados.iterrows():
            departamentos = [d.strip() for d in row['departamento'].split(',')]
            for depto in departamentos:
                if depto in departamentos_selecionados:
                    artigos_dep_expandido.append({'departamento': depto})

        df_departamentos_contagem = pd.DataFrame(artigos_dep_expandido)
        if not df_departamentos_contagem.empty:
            df_departamentos_contagem = df_departamentos_contagem.value_counts().reset_index(name='quantidade')

            fig_bar_depart = px.bar(
                df_departamentos_contagem,
                x='departamento',
                y='quantidade',
                color='departamento',
                text='quantidade',
                title='Artigos Nacionais por Departamento'
            )
            fig_bar_depart.update_layout(showlegend=False, bargap=0.2)
            st.plotly_chart(fig_bar_depart, use_container_width=True)

    st.header("Artigos Internacionais")

    # Filtro de artigos internacionais
    artigos_internacionais_filtrados = artigos[
        (artigos['tipo'] == 'INTERNACIONAL') &
        (artigos['anopubli'].astype(int).between(anos_selecionados[0], anos_selecionados[1])) &
        (artigos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)))
    ]

    # Criando coluna de setor
    artigos_internacionais_setores = artigos_internacionais_filtrados.copy()
    artigos_internacionais_setores['setor'] = artigos_internacionais_setores['departamento'].apply(
        lambda dptos: next(
            (row['setor'] for row in setores.to_dict('records') if any(depto in dptos for depto in [row['departamento']])),
            None
        )
    )

    col1, col2 = st.columns(2)

    # Gráfico de pizza por setor
    with col1:
        setor_counts = artigos_internacionais_setores['setor'].value_counts().reset_index()
        setor_counts.columns = ['setor', 'quantidade']
        fig_pizza_setor = px.pie(
            setor_counts,
            names='setor',
            values='quantidade',
            title='Artigos Internacionais por Setor',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza_setor.update_layout(showlegend=False)
        st.plotly_chart(fig_pizza_setor, use_container_width=True)

    # Gráfico de barra por departamento
    with col2:
        artigos_dep_expandido = []
        for _, row in artigos_internacionais_filtrados.iterrows():
            departamentos = [d.strip() for d in row['departamento'].split(',')]
            for depto in departamentos:
                if depto in departamentos_selecionados:
                    artigos_dep_expandido.append({'departamento': depto})

        df_departamentos_contagem = pd.DataFrame(artigos_dep_expandido)
        if not df_departamentos_contagem.empty:
            df_departamentos_contagem = df_departamentos_contagem.value_counts().reset_index(name='quantidade')

            fig_bar_depart = px.bar(
                df_departamentos_contagem,
                x='departamento',
                y='quantidade',
                color='departamento',
                text='quantidade',
                title='Artigos Internacionais por Departamento'
            )
            fig_bar_depart.update_layout(showlegend=False, bargap=0.2)
            st.plotly_chart(fig_bar_depart, use_container_width=True)

    st.header("Resumos em Congressos")

    # Filtro de resumos em congressos
    resumos_congressos_filtrados = congressos[
        (congressos['tipo'] == 'RESUMO') &
        (congressos['anoconclusao'].astype(int).between(anos_selecionados[0], anos_selecionados[1])) &
        (congressos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)))
    ]

    # Criando coluna de setor
    resumos_setores = resumos_congressos_filtrados.copy()
    resumos_setores['setor'] = resumos_setores['departamento'].apply(
        lambda dptos: next(
            (row['setor'] for row in setores.to_dict('records') if any(depto in dptos for depto in [row['departamento']])),
            None
        )
    )

    col1, col2 = st.columns(2)

    # Gráfico de pizza por setor
    with col1:
        setor_counts = resumos_setores['setor'].value_counts().reset_index()
        setor_counts.columns = ['setor', 'quantidade']
        fig_pizza_setor = px.pie(
            setor_counts,
            names='setor',
            values='quantidade',
            title='Resumos em Congressos por Setor',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza_setor.update_layout(showlegend=False)
        st.plotly_chart(fig_pizza_setor, use_container_width=True)

    # Gráfico de barra por departamento
    with col2:
        congressos_dep_expandido = []
        for _, row in resumos_congressos_filtrados.iterrows():
            departamentos = [d.strip() for d in row['departamento'].split(',')]
            for depto in departamentos:
                if depto in departamentos_selecionados:
                    congressos_dep_expandido.append({'departamento': depto})

        df_departamentos_contagem = pd.DataFrame(congressos_dep_expandido)
        if not df_departamentos_contagem.empty:
            df_departamentos_contagem = df_departamentos_contagem.value_counts().reset_index(name='quantidade')

            fig_bar_depart = px.bar(
                df_departamentos_contagem,
                x='departamento',
                y='quantidade',
                color='departamento',
                text='quantidade',
                title='Resumos em Congressos por Departamento'
            )
            fig_bar_depart.update_layout(showlegend=False, bargap=0.2)
            st.plotly_chart(fig_bar_depart, use_container_width=True)

    st.header("Resumos Expandidos em Congressos")

    # Filtro de resumos expandidos em congressos
    resumos_exp_congressos_filtrados = congressos[
        (congressos['tipo'] == 'RESUMO_EXPANDIDO') &
        (congressos['anoconclusao'].astype(int).between(anos_selecionados[0], anos_selecionados[1])) &
        (congressos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)))
    ]

    # Criando coluna de setor
    resumos_exp_setores = resumos_exp_congressos_filtrados.copy()
    resumos_exp_setores['setor'] = resumos_exp_setores['departamento'].apply(
        lambda dptos: next(
            (row['setor'] for row in setores.to_dict('records') if any(depto in dptos for depto in [row['departamento']])),
            None
        )
    )

    col1, col2 = st.columns(2)

    # Gráfico de pizza por setor
    with col1:
        setor_counts_exp = resumos_exp_setores['setor'].value_counts().reset_index()
        setor_counts_exp.columns = ['setor', 'quantidade']
        fig_pizza_setor_exp = px.pie(
            setor_counts_exp,
            names='setor',
            values='quantidade',
            title='Resumos Expandidos por Setor',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza_setor_exp.update_layout(showlegend=False)
        st.plotly_chart(fig_pizza_setor_exp, use_container_width=True)

    # Gráfico de barra por departamento
    with col2:
        congressos_exp_dep_expandido = []
        for _, row in resumos_exp_congressos_filtrados.iterrows():
            departamentos = [d.strip() for d in row['departamento'].split(',')]
            for depto in departamentos:
                if depto in departamentos_selecionados:
                    congressos_exp_dep_expandido.append({'departamento': depto})

        df_exp_dep_contagem = pd.DataFrame(congressos_exp_dep_expandido)
        if not df_exp_dep_contagem.empty:
            df_exp_dep_contagem = df_exp_dep_contagem.value_counts().reset_index(name='quantidade')

            fig_bar_depart_exp = px.bar(
                df_exp_dep_contagem,
                x='departamento',
                y='quantidade',
                color='departamento',
                text='quantidade',
                title='Resumos Expandidos por Departamento'
            )
            fig_bar_depart_exp.update_layout(showlegend=False, bargap=0.2)
            st.plotly_chart(fig_bar_depart_exp, use_container_width=True)

    st.header("Publicações Completas em Congressos")

    # Filtro de publicações completas
    completo_congressos_filtrados = congressos[
        (congressos['tipo'] == 'COMPLETO') &
        (congressos['anoconclusao'].astype(int).between(anos_selecionados[0], anos_selecionados[1])) &
        (congressos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)))
    ]

    # Criando coluna de setor
    completo_setores = completo_congressos_filtrados.copy()
    completo_setores['setor'] = completo_setores['departamento'].apply(
        lambda dptos: next(
            (row['setor'] for row in setores.to_dict('records') if any(depto in dptos for depto in [row['departamento']])),
            None
        )
    )

    col1, col2 = st.columns(2)

    # Gráfico de pizza por setor
    with col1:
        setor_counts_completo = completo_setores['setor'].value_counts().reset_index()
        setor_counts_completo.columns = ['setor', 'quantidade']
        fig_pizza_setor_completo = px.pie(
            setor_counts_completo,
            names='setor',
            values='quantidade',
            title='Publicações Completas por Setor',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pizza_setor_completo.update_layout(showlegend=False)
        st.plotly_chart(fig_pizza_setor_completo, use_container_width=True)

    # Gráfico de barra por departamento
    with col2:
        congressos_comp_dep_expandido = []
        for _, row in completo_congressos_filtrados.iterrows():
            departamentos = [d.strip() for d in row['departamento'].split(',')]
            for depto in departamentos:
                if depto in departamentos_selecionados:
                    congressos_comp_dep_expandido.append({'departamento': depto})

        df_comp_dep_contagem = pd.DataFrame(congressos_comp_dep_expandido)
        if not df_comp_dep_contagem.empty:
            df_comp_dep_contagem = df_comp_dep_contagem.value_counts().reset_index(name='quantidade')

            fig_bar_depart_completo = px.bar(
                df_comp_dep_contagem,
                x='departamento',
                y='quantidade',
                color='departamento',
                text='quantidade',
                title='Publicações Completas por Departamento'
            )
            fig_bar_depart_completo.update_layout(showlegend=False, bargap=0.2)
            st.plotly_chart(fig_bar_depart_completo, use_container_width=True)

    st.header("Professores com Bolsa Produtividade")

    # Filtrando dados de produtividade pelos filtros principais
    produtividade_filtrada = produtividade[
        (produtividade['ano'].between(anos_selecionados[0], anos_selecionados[1])) &
        (produtividade['departamento'].isin(departamentos_selecionados))
    ]

    # Agrupando por ano e departamento
    prod_por_ano_depto = produtividade_filtrada.groupby(['ano', 'departamento']).size().reset_index(name='quantidade')

    # Gráfico de linha
    fig_linha_produtividade = px.line(
        prod_por_ano_depto,
        x='ano',
        y='quantidade',
        color='departamento',
        markers=True,
        title='Evolução de Professores com Bolsa Produtividade por Departamento'
    )
    fig_linha_produtividade.update_layout(yaxis_title="Quantidade", xaxis_title="Ano")

    st.plotly_chart(fig_linha_produtividade, use_container_width=True)

    # Métrica estilizada com total de professores com bolsa produtividade filtrado
    total_produtividade = len(produtividade_filtrada)

    st.markdown("### Total de Professores com Bolsa Produtividade (com filtros)")
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; text-align:center">
            <h2 style="color:#1f77b4; font-size:48px;">{total_produtividade}</h2>
            <p style="font-size:20px; color:#555;">professores com bolsa produtividade</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with aba2:
        # Filtros
    orientacoes_filtradas = orientacoes[
        orientacoes['departamento'].isin(departamentos_selecionados) &
        orientacoes['anoconclusao'].astype(str).apply(lambda ano: any(str(ano_sel) in ano for ano_sel in range(anos_selecionados[0], anos_selecionados[1] + 1)))
    ]

    bolsas_filtradas = bolsas[
        bolsas['departamento'].isin(departamentos_selecionados) &
        bolsas['ano'].astype(str).apply(lambda ano: any(str(ano_sel) in ano for ano_sel in range(anos_selecionados[0], anos_selecionados[1] + 1)))
    ]

    # Primeira linha: Métricas de orientações
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de orientações (filtros)", len(orientacoes_filtradas))
    with col2:
        st.metric("Total de orientações (UEPG)", len(orientacoes))

    # Segunda linha: Métricas de bolsas
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total de bolsas (filtros)", len(bolsas_filtradas))
    with col4:
        st.metric("Total de bolsas (UEPG)", len(bolsas))

    # Função para pizza por setor
    def grafico_pizza_por_setor(df, titulo):
        # Faz o merge entre o df recebido (orientações ou bolsas) e o df setores
        df_setores = df.merge(setores, on='departamento', how='left')

        # Verifica se há dados após o merge
        if df_setores.empty:
            return None

        # Agrupa por setor e conta
        agrupado = df_setores['setor'].value_counts().reset_index()
        agrupado.columns = ['setor', 'quantidade']

        # Cria o gráfico
        fig = px.pie(
            agrupado,
            names='setor',
            values='quantidade',
            title=titulo,
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        # Formatação para remover legenda lateral e mostrar valores corretamente
        fig.update_layout(showlegend=False)
        fig.update_traces(
            textinfo='label+percent',
            hovertemplate='%{label}: %{value:d}<extra></extra>'
        )

        return fig

    # Função para barra por departamento
    def grafico_barra_depart(df, titulo):
        df_agrupado = df['departamento'].value_counts().reset_index()
        df_agrupado.columns = ['departamento', 'quantidade']
        fig = px.bar(df_agrupado, x='departamento', y='quantidade', color='departamento', text='quantidade', title=titulo)
        fig.update_layout(showlegend=False, bargap=0.2)
        return fig

    # Terceira linha: Iniciação Científica
    inic_cient = orientacoes_filtradas[orientacoes_filtradas['tipo'] == 'INICIAÇÃO CIENTÍFICA']
    col5, col6 = st.columns(2)
    with col5:
        fig1 = grafico_pizza_por_setor(inic_cient, "Iniciação Científica por Setor")
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
    with col6:
        fig2 = grafico_barra_depart(inic_cient, "Iniciação Científica por Departamento")
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)

    # Quarta linha: Pós-graduação (Mestrado + Doutorado)
    pos_grad = orientacoes_filtradas[orientacoes_filtradas['tipo'].isin(['MESTRADO', 'DOUTORADO'])]
    col7, col8 = st.columns(2)
    with col7:
        fig3 = grafico_pizza_por_setor(pos_grad, "Pós-Graduação (Mestrado/Doutorado) por Setor")
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    with col8:
        fig4 = grafico_barra_depart(pos_grad, "Pós-Graduação (Mestrado/Doutorado) por Departamento")
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)

    # Quinta linha: Bolsas de Iniciação Científica
    col9, col10 = st.columns(2)
    with col9:
        fig5 = grafico_pizza_por_setor(bolsas_filtradas, "Bolsas por Setor (IC)")
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)
    with col10:
        fig6 = grafico_barra_depart(bolsas_filtradas, "Bolsas por Departamento (IC)")
        if fig6:
            st.plotly_chart(fig6, use_container_width=True)

with aba3:
    coluna1, coluna2, coluna3 = st.columns(3)

    # Filtro para contar o total de projetos nos devidos departamentos e anos
    total_projetos_selecionados = len(projetos[
        projetos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)) &
        (
          projetos['anopubli'].between(anos_selecionados[0], anos_selecionados[1]) |
          projetos['anopubli'].isna()
        )
    ])

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
            value=len(projetos)
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
                title='Quantidade de Projetos Totais por Departamento'
            )
            # dep_prod_graph.update_traces(visible="legendonly") #Vem marcado tudo no gráfico
            st.plotly_chart(dep_prod_graph, use_container_width=False)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    proj_tipo = proj_tipo[
        proj_tipo['departamento'].apply(
            lambda x: any(depto in x for depto in departamentos_selecionados)
            )
    ]
    #Filtrando projetos por tipo e em seguida removendo o ano
    # PESQUISA
    proj_pesquisa = proj_tipo[(proj_tipo['tipo'] == 'PESQUISA') &
                              (proj_tipo['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))]
    proj_pesquisa_total = proj_pesquisa.groupby(
            ['departamento'], as_index=False
        )['projetos_departamento'].sum()

    proj_extensao = proj_tipo[(proj_tipo['tipo'] == 'EXTENSAO') &
                              (proj_tipo['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))]
    proj_extensao_total = proj_extensao.groupby(
            ['departamento'], as_index=False
        )['projetos_departamento'].sum()

    proj_desenvolvilmento = proj_tipo[(proj_tipo['tipo'] == 'DESENVOLVIMENTO') &
                              (proj_tipo['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))]
    proj_desenvolvilmento_total = proj_desenvolvilmento.groupby(
            ['departamento'], as_index=False
        )['projetos_departamento'].sum()

    proj_ensino = proj_tipo[(proj_tipo['tipo'] == 'ENSINO') &
                              (proj_tipo['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))]
    proj_ensino_total = proj_ensino.groupby(
            ['departamento'], as_index=False
        )['projetos_departamento'].sum()

    proj_outra = proj_tipo[(proj_tipo['tipo'] == 'OUTRA') &
                              (proj_tipo['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))]
    proj_outra_total = proj_outra.groupby(
            ['departamento'], as_index=False
        )['projetos_departamento'].sum()

    grafico_pesquisa = px.bar(
                proj_pesquisa_total,
                x='departamento',
                y='projetos_departamento',
                color='departamento',
                text_auto=True,
                title= 'Projetos de Pesquisa',
                barmode='relative'
            )
    grafico_pesquisa.update_layout(showlegend=False, bargap=0)

    grafico_extensao = px.bar(
                proj_extensao_total,
                x='departamento',
                y='projetos_departamento',
                color='departamento',
                text_auto=True,
                title= 'Projetos de Extensão',
                barmode='relative'
            )
    grafico_extensao.update_layout(showlegend=False, bargap=0)

    grafico_desenvolvimento = px.bar(
                proj_desenvolvilmento_total,
                x='departamento',
                y='projetos_departamento',
                color='departamento',
                text_auto=True,
                title= 'Projetos de Desenvolvimento',
                barmode='relative'
            )
    grafico_desenvolvimento.update_layout(showlegend=False, bargap=0)

    grafico_ensino = px.bar(
                proj_ensino_total,
                x='departamento',
                y='projetos_departamento',
                color='departamento',
                text_auto=True,
                title= 'Projetos de Ensino',
                barmode='relative'
            )
    grafico_ensino.update_layout(showlegend=False, bargap=0)

    grafico_outra = px.bar(
                proj_outra_total,
                x='departamento',
                y='projetos_departamento',
                color='departamento',
                text_auto=True,
                title= 'Outros',
                barmode='relative'
            )
    grafico_outra.update_layout(showlegend=False, bargap=0)

    coluna4, coluna5 = st.columns(2)

    with coluna4:
        if departamentos_selecionados:
            st.plotly_chart(grafico_pesquisa)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    with coluna5:
        if departamentos_selecionados:
            st.plotly_chart(grafico_extensao)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    coluna6, coluna7 = st.columns(2)

    with coluna6:
        if departamentos_selecionados:
            st.plotly_chart(grafico_desenvolvimento)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    with coluna7:
        if departamentos_selecionados:
            st.plotly_chart(grafico_ensino)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    coluna8, coluna9 = st.columns(2)

    with coluna8:
        if departamentos_selecionados:
            st.plotly_chart(grafico_outra)
        else:
            st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    with coluna9:
        st.warning('Aguardando projetos de pesquisa continuada...')

    coluna10, coluna11 = st.columns(2)

    # Filtrando a tabela "financiados" com os filtros do sidebar
    financiados_filtrados = financiados[
        (financiados['departamento'].isin(departamentos_selecionados)) &
        (financiados['anopubli'].between(anos_selecionados[0], anos_selecionados[1]))
    ]


    with coluna10:
        st.metric(
            'Total de projetos com financimento (UEPG):',
            len(financiados)
        )

        st.metric(
            'Total de projetos com financiamento (Filtros):',
            len(financiados_filtrados)
        )

    with coluna11:
        valor_total_uepg = sum(financiados['valor'])
        valor_formatado_uepg = f"R$ {valor_total_uepg:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        st.metric(
            'Valor total recebido de projetos financiados (UEPG):',
            valor_formatado_uepg
        )

        # Calculando o valor total arrecadado
        valor_total = financiados_filtrados['valor'].sum()

        # Formatando para o padrão brasileiro (ex: 1.000.000,50)
        valor_formatado = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # Exibir métrica no Streamlit
        st.metric(label="Valor total recebido de projetos financiados (Filtros)", value=valor_formatado)

with aba4:
    # st.write(f'departamentos: {departamentos_selecionados} TIPO: {type(departamentos_selecionados)}')
    # st.write(f'anos: {anos_selecionados} TIPO: {type(anos_selecionados)}')
    # st.write(f'anos: {anos_selecionados[0]} até {anos_selecionados[1]}')
    professores_efetivos = professores[professores['status'] == 'EFETIVO']

    col1, col2 = st.columns(2)

    # Filtrando os professores conforme os departamentos e anos selecionados
    professores_filtrados = professores_efetivos[
        professores_efetivos['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)) &  # Filtro de departamentos
        professores_efetivos['anosuepg'].apply(
            lambda anos: any(
                ano in range(anos_selecionados[0], anos_selecionados[1] + 1) for ano in ast.literal_eval(anos)  # Converte a string para um conjunto/lista e filtra
            )
        )
        ]
    # st.dataframe(professores_filtrados)
    with col1:
        st.metric(
            "Total de professores (departamentos selecionados)",
            len(professores_filtrados)
        )

    with col2:
        st.metric(
            "Total de professores efetivos da UEPG: ",
            len(professores_efetivos)
        )

    # Criando os dataframes por titulação
    graduados = professores_filtrados[professores_filtrados['graduacao'] == 'Graduado']
    mestres = professores_filtrados[professores_filtrados['graduacao'] == 'Mestre']
    doutores = professores_filtrados[professores_filtrados['graduacao'] == 'Doutor']

    # Função para criar gráfico de pizza
    def criar_grafico_pizza(df, titulo):
        if df.empty:
            return None
        df_agrupado = df.groupby('departamento').size().reset_index(name='quantidade')
        return px.pie(
            df_agrupado,
            names='departamento',
            values='quantidade',
            title=titulo,
            color_discrete_sequence=px.colors.qualitative.Set3
        )

    # Criando os gráficos
    grafico_graduado = criar_grafico_pizza(graduados, "Professores GRADUADOS por Departamento")
    grafico_mestre = criar_grafico_pizza(mestres, "Professores MESTRES por Departamento")
    grafico_doutor = criar_grafico_pizza(doutores, "Professores DOUTORES por Departamento")

    st.subheader("Distribuição de Titulação por Departamento")

    if grafico_graduado:
        st.plotly_chart(grafico_graduado)
    else:
        st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    if grafico_mestre:
        st.plotly_chart(grafico_mestre)
    else:
        st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

    if grafico_doutor:
        st.plotly_chart(grafico_doutor)
    else:
        st.warning("Selecione pelo menos um departamento para visualizar o gráfico.")

with aba5:
    st.header("Perfil dos Professores")

    # Gráficos sem filtros - Pizza por setor e por departamento
    col1, col2 = st.columns(2)

    with col1:
        fig_setor = px.pie(professores, names='setor', title="Distribuição por Setor", hole=0.4)
        st.plotly_chart(fig_setor, use_container_width=True)

    with col2:
        fig_departamento = px.pie(professores, names='departamento', title="Distribuição por Departamento", hole=0.4)
        fig_departamento.update_layout(showlegend = False)
        st.plotly_chart(fig_departamento, use_container_width=True)

    # Aplicando filtros
    prof_filtrado = professores[
        professores['departamento'].isin(departamentos_selecionados) &
        professores['anosuepg'].apply(lambda x: any(str(ano) in x for ano in range(anos_selecionados[0], anos_selecionados[1] + 1)))
    ]

    # 1ª Linha: EFETIVO
    efetivos = prof_filtrado[prof_filtrado['status'] == 'EFETIVO']
    col1, col2 = st.columns(2)
    with col1:
        fig_efetivo_setor = px.bar(
            efetivos.groupby('setor').size().reset_index(name='quantidade'),
                x='setor', 
                y='quantidade', 
                text='quantidade', 
                title='Efetivos por Setor', 
                color='setor'
        )
        fig_efetivo_setor.update_layout(bargap=0, showlegend = False)
        st.plotly_chart(fig_efetivo_setor, use_container_width=True)

    with col2:
        fig_efetivo_depart = px.bar(
            efetivos.groupby('departamento').size().reset_index(name='quantidade'),
                x='departamento', 
                y='quantidade', 
                text='quantidade', 
                title='Efetivos por Departamento',
                color='departamento'
        )
        fig_efetivo_depart.update_layout(bargap=0, showlegend=False)
        st.plotly_chart(fig_efetivo_depart, use_container_width=True)

    # 2ª Linha: COLABORADOR
    colaboradores = prof_filtrado[prof_filtrado['status'] == 'COLABORADOR']
    col1, col2 = st.columns(2)
    with col1:
        fig_colab_setor = px.bar(
            colaboradores.groupby('setor').size().reset_index(name='quantidade'),
                x='setor', 
                y='quantidade', 
                text='quantidade', 
                title='Contratos de Colaboradores por Setor',
                color='setor'
        )
        fig_colab_setor.update_layout(bargap=0)
        st.plotly_chart(fig_colab_setor, use_container_width=True)

    with col2:
        fig_colab_depart = px.bar(
            colaboradores.groupby('departamento').size().reset_index(name='quantidade'),
                x='departamento', 
                y='quantidade', 
                text='quantidade', 
                title='Contratos de Colaboradores por Departamento',
                color='departamento'
        )
        fig_colab_depart.update_layout(bargap=0, showlegend=False)
        st.plotly_chart(fig_colab_depart, use_container_width=True)

    # 3ª Linha: Métrica TIDE
    quantidade_tide = prof_filtrado[prof_filtrado['tide'].str.lower() == 'sim'].shape[0]
    st.markdown("""
        <div style='text-align: center;'>
            <h3>Quantidade de professores em dedicação exclusiva - TIDE</h3>
            <h1 style='color: green;'>{}</h1>
        </div>
    """.format(quantidade_tide), unsafe_allow_html=True)  
