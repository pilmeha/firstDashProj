from dash import html, dcc
import plotly.express as px

def generate_layout(df):
    fig = px.bar(df, x="Участник", y="% выполнения", color="Группа", barmode="group",
                 title="Выполнение плана по участникам")
    
    return html.Div(id='graph_layout',children=[
        html.H2("Дашборд выполнения плана продаж по группам"),
        dcc.Graph(figure=fig),
    ])
