import streamlit as st
import ast
import plotly.express as px
from graphs import dep_prod_graph
from utils import (artigos, bolsas, congressos, financiados, orientacoes, 
                   produtividade, professores, projetos, setores, dep_prod, 
                   dataframes_col_anos, proj_tipo)

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
                title='Produção Total Por Departamento'
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
    st.write(f'departamentos: {departamentos_selecionados} TIPO: {type(departamentos_selecionados)}')
    st.write(f'anos: {anos_selecionados} TIPO: {type(anos_selecionados)}')
    st.write(f'anos: {anos_selecionados[0]} até {anos_selecionados[1]}')

    # Filtrando os professores conforme os departamentos e anos selecionados
    professores_filtrados = professores[
        professores['departamento'].apply(lambda x: any(depto in x for depto in departamentos_selecionados)) &  # Filtro de departamentos
        professores['anosuepg'].apply(
            lambda anos: any(
                ano in range(anos_selecionados[0], anos_selecionados[1] + 1) for ano in ast.literal_eval(anos)  # Converte a string para um conjunto/lista e filtra
            )
        )
        ]
    st.dataframe(professores_filtrados)

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
    grafico_graduado = criar_grafico_pizza(graduados, "Professores Graduados por Departamento")
    grafico_mestre = criar_grafico_pizza(mestres, "Professores Mestres por Departamento")
    grafico_doutor = criar_grafico_pizza(doutores, "Professores Doutores por Departamento")

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