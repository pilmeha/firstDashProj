from dash import html, dcc

def generate_scores_layout(df):
    c=0
    for g in df:
        if g.calculateCurrProc()>=g.minProc and g.calculateCompleteCount()>=g.minMemb:
            c+=g.score
    
    return html.Div(id='scores_layout',style={'display': 'none'},children=[
           html.Div(id='score-container',children='Текущее количество баллов: '+str(c))
        ])

