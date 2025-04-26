import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from utils.rules_engine import apply_rules
from components.layout import generate_layout
from components.dr_layout import generate_dynamic_rules_layout
from components.sc_layout import generate_scores_layout
from utils.xlsxParser import load_groups_from_excel
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

group_objs = load_groups_from_excel("data/xlsxParser.xlsx")

crossRibates=[0,0,0]

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
                "Требуемое кол-во выполненных разделов": g.minMemb,
                "% выполнения (общий)": g.calculateCurrProc(),
                "Кол-во выполненных разделов": g.calculateCompleteCount(),
                "Балл за группу": g.score,
                "Регион": m.region,
            })
    return pd.DataFrame(rows)

processed_df = groups_to_dataframe(group_objs)

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Графики', value='tab-1'),
        dcc.Tab(label='Динамические правила', value='tab-2'),
        dcc.Tab(label='Баллы', value='tab-3')
    ]),
    html.Div(id='tabs-content',children=[
        generate_layout(processed_df),
        generate_dynamic_rules_layout(group_objs),
        generate_scores_layout(group_objs)
    ])
    ],
    style={
        'margin-left': '80px',
        'margin-right': '80px',
}
)

@app.callback(
    Output('graph_layout', 'style'),
    Output('rules_layout', 'style'),
    Output('scores_layout', 'style'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return ({'display': 'block'},{'display': 'none'},{'display': 'none'})
    elif tab == 'tab-2':
        return ({'display': 'none'},{'display': 'block'},{'display': 'none'})
    elif tab == 'tab-3':
        return ({'display': 'none'},{'display': 'none'},{'display': 'block'})

@app.callback(
    Output('output-container1', 'children'),
    Output('crossRibate', 'children',allow_duplicate=True),
    Input('names1', 'value'),
    Input('proc1', 'value'),
    Input('cros1', 'value'),
    prevent_initial_call=True,
)
def update_output1(names,proc,cros):
    return ruleOut(names,proc,cros,0)

@app.callback(
    Output('output-container2', 'children'),
    Output('crossRibate', 'children',allow_duplicate=True),
    Input('names2', 'value'),
    Input('proc2', 'value'),
    Input('cros2', 'value'),
    prevent_initial_call=True,
)
def update_output2(names,proc,cros):
    return ruleOut(names,proc,cros,1)

@app.callback(
    Output('output-container3', 'children'),
    Output('crossRibate', 'children',allow_duplicate=True),
    Input('names3', 'value'),
    Input('proc3', 'value'),
    Input('cros3', 'value'),
    prevent_initial_call=True,
)
def update_output3(names,proc,cros):
    return ruleOut(names,proc,cros,2)
    
def ruleOut(names,proc,cros,i):
    prCurr=''
    prPlan=''
    prProc=''
    for g in group_objs:
        for m in g.members:
            if m.name==names:
                prPlan=str(m.plan)
                prCurr=str(m.current)
                prProc=str(m.proc*100)
    if float(prProc)>=int(proc):
        crossRibates[i]=float(cros)
        return ('Процент по продукту '+names+' >= заданного ('+prProc+'), кросс-рибейт +'+cros+'%','Сумма кросс-рибейта: '+str(sum(crossRibates))+'%')
    else:
        crossRibates[i]=0
        return ('Процент по продукту '+names+' недостаточен ('+prProc+')','Сумма кросс-рибейта: '+str(sum(crossRibates))+'%')

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run(debug=True)

