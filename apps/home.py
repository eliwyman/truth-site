import dash
from dash import dcc
from dash import html

import os

from apps import bot_helper

app = dash.Dash(
    __name__,
    requests_pathname_prefix='/app/'
)

#def display(app):

helper = bot_helper.Helper()

app.layout = html.Div([
    dcc.Markdown('### Application Index Page'),

    html.Div([
        helper.get_nav_div_server()
    ]),  
])

server = app.server
