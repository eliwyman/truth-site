import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

from apps import bot_helper

helper = bot_helper.Helper()