import plotly.express as px
from utils import (artigos ,bolsas,congressos,financiados,orientacoes,
                   produtividade ,professores , projetos, dep_prod)

print(dep_prod)

dep_prod_graph = px.line(
    dep_prod,
    x='anopubli',
    y='quantidade_prod',
    color='departamento',
    range_y=(0, dep_prod['quantidade_prod'].max()),
    line_dash='departamento',
    title='Produção por Departamento'
)
dep_prod_graph.update_traces(visible="legendonly")