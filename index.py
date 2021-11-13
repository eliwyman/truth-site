from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import home, us_crime, covid_israel_study
        
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/apps/us_crime':
        return us_crime.layout
    elif pathname == '/apps/covid_israel_study':
        return covid_israel_study.layout
    elif pathname in ['/', '/home', '/index', '/index.html', '/index.py', '/apps/', '/apps/home']:
        return home.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)