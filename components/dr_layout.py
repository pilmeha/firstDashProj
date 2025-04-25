from dash import html, dcc

def generate_dynamic_rules_layout(df):
    groupNames=[g.name for g in df]
    productNames=[]
    for g in df:
        for m in g.members:
            productNames.append(m.name)
    
    return html.Div(id='rules_layout',style={'display': 'none'},children=[
           dcc.Dropdown(
               id='names1',
               options=[{'label': n, 'value': n} for n in productNames],
               value=productNames[0] # The default value to display
           ),
            dcc.Dropdown(
                id='proc1',
                options=[{'label': str(n), 'value': str(n)} for n in range(101)],
                value='100' # The default value to display
           ),
           dcc.Dropdown(
                id='cros1',
                options=[{'label': str(n/10), 'value': str(n/10)} for n in range(1,21)],
                value='1.0' # The default value to display
           ),
           html.Div(id='output-container1'),

           dcc.Dropdown(
               id='names2',
               options=[{'label': n, 'value': n} for n in productNames],
               value=productNames[0] # The default value to display
           ),
            dcc.Dropdown(
                id='proc2',
                options=[{'label': str(n), 'value': str(n)} for n in range(101)],
                value='100' # The default value to display
           ),
           dcc.Dropdown(
                id='cros2',
                options=[{'label': str(n/10), 'value': str(n/10)} for n in range(1,21)],
                value='1.0' # The default value to display
           ),
           html.Div(id='output-container2'),

           dcc.Dropdown(
               id='names3',
               options=[{'label': n, 'value': n} for n in productNames],
               value=productNames[0] # The default value to display
           ),
            dcc.Dropdown(
                id='proc3',
                options=[{'label': str(n), 'value': str(n)} for n in range(101)],
                value='100' # The default value to display
           ),
           dcc.Dropdown(
                id='cros3',
                options=[{'label': str(n/10), 'value': str(n/10)} for n in range(1,21)],
                value='1.0' # The default value to display
           ),
           html.Div(id='output-container3'),
           html.Div('====================================================='),
           html.Div(id='crossRibate'),
        ])

