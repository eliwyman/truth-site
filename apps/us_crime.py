from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# hide certain plotly functions(buttons) from bar charts
bar_config={
    'modeBarButtonsToRemove': ['zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
}

from app import app

# filepath needs to be relative to app.py (engine)
fbi_state_df = pd.read_csv('data/fbi_state_summary.csv')
fbi_df = pd.read_csv('data/FBI_all_offenses.csv')
ojjdp_df = pd.read_csv('data/OJJDP_all_offenses.csv')

layout = html.Div([
    
    dcc.Markdown('''
    
    # U.S. Federal Crime Analysis
    
'''),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label" : x, "value" : x} for x in fbi_df.drop(['Year', 'Population'], axis=1).columns],
        value=fbi_df.columns[0],
        clearable=False,
    ),
    dcc.Graph(id="bar-chart", config=bar_config),
    dash_table.DataTable(
        id='tbl',
        columns=[{"name": i, "id": i} for i in fbi_state_df.columns],
        data=fbi_state_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        
        # left align text for readability
        style_cell={'textAlign': 'left'},
        
        # wrap text in data (non-header) cells
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    ),
    html.Br(),
    dcc.Link('Go to Israel Covid-19 Study', href='/apps/covid_israel_study'),
    
    dcc.Markdown('''
    
    > This data was taken from ... 
    
''')    
])

@app.callback(
    Output("bar-chart", "figure"), 
    Input("dropdown", "value"))

def update_bar_chart(category):
    
    fig = px.bar(fbi_df, x='Year', y=category,
                hover_data=[category]
                )
    
    fig.add_trace(
        go.Scatter(
            x=fbi_df.Year,
            y=fbi_df[category],
            name='trendline'
    ))
    
    fig.update_layout(xaxis_tickangle=-45)

    
    return fig