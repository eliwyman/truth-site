from flask import Flask, request, render_template

def init_app():
    app_name = 'frontend'
    print('app_name = {}'.format(app_name))

    # create app
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def display_index():
        return render_template('index.html')

    return app
