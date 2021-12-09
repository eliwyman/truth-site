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

import os

from app import app, helper

# filepath needs to be relative to app.py (engine)
fbi_state_df = pd.read_csv('data/fbi_state_summary.csv')
fbi_df = pd.read_csv('data/FBI_all_offenses.csv')
ojjdp_df = pd.read_csv('data/OJJDP_all_offenses.csv')

layout = html.Div([
    
    dcc.Markdown('''
    # U.S. Federal Crime
'''),
    dcc.Dropdown(
        id="dropdown-fbi",
        options=[{"label" : x, "value" : x} for x in fbi_df.drop(['Year', 'Population'], axis=1).columns],
        value=fbi_df.columns[0],
        clearable=False,
    ),
    dcc.Graph(id="fbi-bar-chart", config=bar_config),
    
    dcc.Dropdown(
        id="dropdown-ojp",
        options=[{"label" : 'All offenses', "value" : 'All offenses'}],
        value='All offenses',
        clearable=False,
    ),
    dcc.Graph(id="ojp-bar-chart", config=bar_config),
    
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

    html.Div([
        helper.get_nav_div(os.path.splitext(os.path.basename(__file__))[0])
    ]),  
    
    dcc.Markdown('''
    
    > This app serves to display U.S. Federal Crime data, collected from both the Federal Bureau of Investigation (FBI), and the  Office of Juvenile Justice and Deliquency Program (OJJDP). 
    
    > [OJJDP Arrests by offense, age, and gender](https://www.ojjdp.gov/ojstatbb/crime/ucr.asp)
    
    > [FBI Crime in the U.S.](https://ucr.fbi.gov/crime-in-the-u.s/)
    
    > Including the results of k-means clustering machine learning algorithm, designed to establish a State ranking for crime levels, by analyzing U.S. County crime reports. 
    
''')    
])

@app.callback(
    Output("fbi-bar-chart", "figure"), 
    Input("dropdown-fbi", "value"))

def update_fbi_bar_chart(category):
    
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

@app.callback(
    Output("ojp-bar-chart", "figure"), 
    Input("dropdown-ojp", "value"))

def update_ojp_bar_chart(category):
    
    fig = px.bar(ojjdp_df, x='Year', y=category,
                hover_data=[category]
                )
    
    fig.add_trace(
        go.Scatter(
            x=ojjdp_df.Year,
            y=ojjdp_df[category],
            name='trendline'
    ))
    
    fig.update_layout(xaxis_tickangle=-45)

    
    return fig