import plotly.express as px
from utils import (artigos ,bolsas,congressos,financiados,orientacoes,
                   produtividade ,professores , projetos, dep_prod)

# PRODUÇÃO POR DEPARTAMENTO
dep_prod_graph = px.line(
    dep_prod,
    x='anopubli',
    y='projetos_departamento',
    color='departamento',
    range_y=(0, dep_prod['projetos_departamento'].max()),
    line_dash='departamento',
    title='Produção por Departamento'
)
dep_prod_graph.update_traces(visible="legendonly")