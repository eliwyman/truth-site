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

import os

from apps import bot_helper

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/us_mortality/'
)

helper = bot_helper.Helper()

usd = pd.read_csv(helper.APP_ROOT + '/data/us_deaths_by_cause.csv', index_col = 0)

# column definitions for the models
definitions = ['Rank',
    'Cause of death',
    'Classification code',
    '2018 Number',
    '2018 Percent',
    '2018 Rate',
    '2019 Number',
    '2019 Percent',
    '2019 Rate']

app.layout = html.Div([
    
    dcc.Markdown('''
    # US Deaths by Cause
'''),
    dcc.Graph(id="usd_bar-chart", config=bar_config),
    dash_table.DataTable(
        id='usd_tbl',
        columns=[{"name": i, "id": i} for i in usd.columns],
        data=usd.to_dict('records'),
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
    dbc.Alert(id='usd_tbl_out'),
    html.Br(),

    html.Div([
        helper.get_nav_div(os.path.splitext(os.path.basename(__file__))[0])
    ]),
    
    dcc.Markdown('''
    
    > This app serves to display the data from the National Center for Health Statistics, National Vital Statistics System, Mortality.
    
    > This data was taken from the NCHS Data Brief No. 395, table 4
         https://www.cdc.gov/nchs/data/databriefs/db395-tables-508.pdf#page=4
         
    > Publically accessible via the CDC website at 
        https://www.cdc.gov/nchs/products/databriefs/db395.htm
''')
    
])

@app.callback(
    Output("usd_bar-chart", "figure"), 
    Input("usd_tbl", "value"))

def update_bar_chart(model):
    fig = px.bar(usd, x='Cause of death', y=['2018 Number', '2019 Number'], barmode="group")

    return fig

@app.callback(
    Output('usd_tbl_out', 'children'),
    Input('usd_tbl', 'active_cell'))

def update_table(active_cell):
    return definitions[active_cell['column']] if active_cell else "Click the table"

server = app.server