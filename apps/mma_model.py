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
dash_config={
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
}

import os

from apps import bot_helper

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/mma_model/'
)

helper = bot_helper.Helper()

mma = pd.read_csv(helper.APP_ROOT + '/data/fighter_report_UFC_2020.csv', index_col = 0)
mma = mma.drop(['FighterId'], axis=1)

app.layout = html.Div([
    
    dcc.Markdown('''
    # MMA Fighter Stats (UFC 2020)
    
    Through the use of a multiple regression model (analysis showed RandomForestRegressor to perform best),
    the following attributes were highest correlated with wins, in this order.
    
    DecisionPercentage: the percentage of wins by decision
    
    TechnicalKnockoutPercentage: the percentage of wins by KO
    
    StrikeFinishPercentage: the percentage of wins by either TKO or KO
    
    WorkAverage: how often a fighter is making submission attempts, throwing strikes, or completing take downs
    
    ### Select a stat from the dropdown below to see it's distribution amongst fighters.
'''),
    
    dcc.Dropdown(
        id="dropdown-mma",
        options=[
            {"label" : 'Decision Percentage', "value" : 'DecisionPercentage'},
            {"label" : 'Strike Finish Percentage', "value" : 'StrikeFinishPercentage'},
            {"label" : 'Work Average', "value" : 'WorkAverage'}
        ],
        value='DecisionPercentage',
        clearable=False,
    ),
    dcc.Graph(id="mma-histogram", config=dash_config),
    
    dash_table.DataTable(
        id='mma_tbl',
        columns=[{"name": i, "id": i} for i in mma.columns],
        data=mma.to_dict('records'),
        style_table={'overflowX': 'auto'},
        
        # left align text in header row for readability
        style_header={'textAlign': 'left'},
        
        # wrap text in data (non-header) cells
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        page_size=10
    ),
    
    dcc.Markdown('''
    
    > This app serves to display fighter data from UFC's 2020 events.
    
    > The data is available through an API at: https://sportsdata.io
    
    > API documentation for this set: https://sportsdata.io/developers/api-documentation/mma#/sports-data
'''),

    html.Div([
        helper.get_nav_div_server()
    ]) 
    
])

@app.callback(
    Output("mma-histogram", "figure"), 
    Input("dropdown-mma", "value"))

def show_mma_histogram(category):
        
    fig = go.Figure(data=[go.Histogram(x=mma[category])])
    
    return fig

server = app.server
