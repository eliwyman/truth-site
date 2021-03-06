from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app import init_app as app_frontend_init_app

from apps import home, us_crime, covid_israel_study, us_mortality, mma_model

frontend = app_frontend_init_app()

application = DispatcherMiddleware(frontend, {
    '/app': home.server,
    '/us_crime': us_crime.server,
    '/covid_israel_study': covid_israel_study.server,
    '/us_mortality': us_mortality.server,
    '/mma_model': mma_model.server
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)
