import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.rules_engine import apply_rules
from components.layout import generate_layout
from utils.xlsxParser import load_groups_from_excel
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

group_objs = load_groups_from_excel("data/xlsxParser.xlsx")

# Преобразуем в pandas DataFrame для визуализации
def groups_to_dataframe(groups):
    rows = []
    for g in groups:
        for m in g.members:
            rows.append({
                "Группа": g.name,
                "Участник": m.name,
                "План": m.plan,
                "Факт": m.current,
                "% выполнения": round(m.proc * 100, 1),
                "Требуемый % выполнения": g.minProc,
                "Требуемое кол-во выполненных": g.minMemb,
                "Балл за группу": g.score
            })
    return pd.DataFrame(rows)

processed_df = groups_to_dataframe(group_objs)

app.layout = generate_layout(processed_df)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=True)

