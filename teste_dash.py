from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from import_db import dep_prod_df

df = dep_prod_df
app = Dash()

app.layout = [
    html.H1(children = 'Produção por departamento', style={'textAlign': 'center'}),
    dcc.Dropdown(df.departamento.unique(), 'Departamento de Zootecnia', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.departamento==value]
    return px.line(dff, x='anopubli', y='quantidade_produ')

if __name__ == '__main__':
    app.run(debug=True)
