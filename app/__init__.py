from flask import Flask, request, render_template

def init_app():
    app_name = 'frontend'
    print('app_name = {}'.format(app_name))

    # create app
    app = Flask(__name__)

    # define folder name for static files (CSS, JS, etc.)
    app.static_folder = 'static'

    @app.route("/")
    def display_index():
        return render_template('index.html')

    return app
