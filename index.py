from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import home, app1, app2, covid_israel_study
        
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/covid-israel-study':
        return covid_israel_study.layout
    elif pathname in ['/', '/home', '/index', '/index.html', '/index.py', '/apps/']:
        return home.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)