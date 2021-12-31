To run the app in production, the recommended approach is to use Apache to handle the requests to the Flask application, that serves the dash applications using a Dispatcher. The contents of app.wsgi are shown below for this approach:

# app.wsgi

#!/usr/bin/python
import sys
sys.path.insert(0, '/home/edwadmin/site')

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from app import init_app as app_frontend_init_app

from apps import home, us_crime, covid_israel_study

frontend = app_frontend_init_app()

application = DispatcherMiddleware(frontend, {
    '/app': home.server,
    '/us_crime': us_crime.server,
    '/covid_israel_study': covid_israel_study.server,
})


To run the app in development:

	With Dash development tools (run this line for each app):

		> app1.enable_dev_tools(debug=True)

	In either scenario:

		> python run.py
