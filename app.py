import dash
from dash import dcc, html
import dash.dependencies as dd
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# Conexão com o banco de dados
# Conexão com o banco de dados usando SQLAlchemy
def get_data():
    engine = create_engine("postgresql+psycopg2://postgres:Gumattos2@localhost:5432/banco2")
    query = "SELECT * FROM professores LIMIT 100;"
    df = pd.read_sql_query(query, con=engine)
    return df

# Carregar os dados
df = get_data()

# Criar a aplicação Dash
app = dash.Dash(__name__)

# Layout do Dashboard
app.layout = html.Div([
    html.H1("Meu Dashboard Interativo"),
    dcc.Dropdown(
        id="filtro",
        options=[{"label": col, "value": col} for col in df.columns],
        value=df.columns[0]
    ),
    dcc.Graph(id="grafico"),
])

# Callback para atualizar o gráfico
@app.callback(
    dd.Output("grafico", "figure"),
    [dd.Input("filtro", "value")]
)
def atualizar_grafico(coluna):
    fig = px.bar(df, x="nome", y=coluna)
    return fig

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)