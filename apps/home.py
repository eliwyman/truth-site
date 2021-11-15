from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import os

from app import app, helper

layout = html.Div([
    dcc.Markdown('''
    ### Homepage

    Please **click** one of the links below to explore our app library.
    '''),
    
    html.Div([
        helper.get_nav_div(os.path.splitext(os.path.basename(__file__))[0])
    ]),  
])