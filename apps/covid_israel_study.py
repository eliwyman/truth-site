import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc

import pandas as pd

import os

import plotly.express as px
import plotly.graph_objects as go

# hide certain plotly functions(buttons) from bar charts
bar_config={
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
}

from apps import bot_helper

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/covid_israel_study/'
)

helper = bot_helper.Helper()

sc = pd.read_csv(helper.APP_ROOT + '/data/study_characteristics.csv')
odds_m1_m2 = pd.read_csv(helper.APP_ROOT + '/data/odds_ratios_m1_m2.csv', header = 0, index_col = 0)
odds_m3 = pd.read_csv(helper.APP_ROOT + '/data/odds_ratios_m3.csv', header = 0, index_col = 0)

# column definitions for the models
definitions = ['Model',
               'Study participant count (total)',
               'Average age',
               'Average age SD – Standard Deviation',
               'Study participant count (age 16 to 39)',
               'Study participant % (age 16 to 39)',
               'Study participant count (age 40 to 59)',
               'Study participant % (age 40 to 59)',
               'Study participant count (age 60+)',
               'Study participant % (age 60+)',
               'Study participant count (sex Female)',
               'Study participant % (sex Female)',
               'Study participant count (sex Male)',
               'Study participant % (sex Male)',
               'Socioeconomic status on a scale from 1 (lowest) to 10',
               'Socioeconomic status on a scale from 1 (lowest) to 10 - SD - Standard Deviation']

app.layout = html.Div([
    
    dcc.Markdown('''
    # Israel Covid Study
'''),
    
    dash_table.DataTable(
        id='tbl',
        columns=[{"name": i, "id": i} for i in sc.columns],
        data=sc.to_dict('records'),
        style_table={'overflowX': 'auto'},
        
        # left align text in header row for readability
        style_header={'textAlign': 'left'},
        
        # wrap text in data (non-header) cells
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    ),
    html.Br(),
    dbc.Alert(id='tbl_out'),
    html.Br(),
    dcc.Dropdown(
        id="dropdown1",
        options=[{"label" : x, "value" : x} for x in odds_m1_m2.columns],
        value=odds_m1_m2.columns[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart1", config=bar_config),
    html.Br(),
    dcc.Dropdown(
        id="dropdown2",
        options=[{"label" : x, "value" : x} for x in odds_m3.columns],
        value=odds_m3.columns[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart2", config=bar_config),
    
    html.Div([
        helper.get_nav_div_server()
    ]),
    
    dcc.Markdown('''
    
    > This app serves to display the data from the study titled 'Comparing SARS-CoV-2 natural immunity to vaccine-induced immunity: reinfections versus breakthrough infections'
    
    > This data was taken from this published study https://www.medrxiv.org/content/10.1101/2021.08.24.21262415v1.full.pdf on November 8th, 2021  
    > Referenced in the article published on MedRxiv https://doi.org/10.1101/2021.08.24.21262415
''')
    
])

#def init_callbacks(app):
@app.callback(
    Output("bar-chart1", "figure"), 
    Input("dropdown1", "value"))

def update_bar_chart1(model):
    fig = px.bar(odds_m1_m2, x=odds_m1_m2.index, y=model,
                color=model,
                hover_data=[model]
    )
    
    return fig

@app.callback(
    Output("bar-chart2", "figure"), 
    Input("dropdown2", "value"))

def update_bar_chart2(model):
    fig = px.bar(odds_m3, x=odds_m3.index, y=model,
                color=model,
                hover_data=[model]
    )

    return fig

@app.callback(
    Output('tbl_out', 'children'),
    Input('tbl', 'active_cell'))

def update_table(active_cell):
    return definitions[active_cell['column']] if active_cell else "Click the table"

server = app.server
