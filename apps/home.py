from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    dcc.Markdown('''
    ### Homepage

    Please **click** one of the links below to explore our app library.
    '''),
    dcc.Link('Go to App 1', href='/apps/app1'),
    html.Br(),
    dcc.Link('Go to App 2', href='/apps/app2'),
    html.Br(),
    dcc.Link('Go to covid-israel-study', href='/apps/covid-israel-study')    
])