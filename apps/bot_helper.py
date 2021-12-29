import os
import fnmatch

import re

from dash import dcc
from dash import html

class Helper:
    '''
    Burden of Truth custom helper class
    '''
    # constructor of Main class
    def __init__(self):
        # Initialization of the Strings
        print("Class 'help_class' v1 has been loaded")

    def find_apps(self, pattern, top = '/home/edwadmin/site/apps/'):
        result = []
        for root, dirs, files in os.walk(top):
            for name in files:
                if fnmatch.fnmatch(name, pattern) \
                and not fnmatch.fnmatch(name, '__init__.py') \
                and not fnmatch.fnmatch(name, 'bot_helper.py'):
                    result.append(os.path.splitext(name))
        return result       
        
    def get_nav_div(self, curr: str):
        '''
        This function takes the name of an app as a string, and returns a Dash html div object
        for site navigation from that page (omitting that page from the links).
        '''
        app_names = self.find_apps('*.py')
        nav_links = []
        
        for app in app_names:
            if app != curr:
                nav_links.append(dcc.Link('Go to ' + app, href='/apps/' + app))
                nav_links.append(html.Br())
                
        nav_div = html.Div(
            nav_links
        )
        
        return nav_div
    
    def get_nav_div_server(self):
        '''
        This function returns a Dash html div object for site navigation. 
        '''
        nav_links = []
        
        nav_links.append(dcc.Link('Go to Covid Israel Study', href='/covid_israel_study/', target="_blank"))
        nav_links.append(html.Br())
        nav_links.append(dcc.Link('Go to US Crime', href='/us_crime/', target="_blank"))
        nav_links.append(html.Br())
        nav_links.append(dcc.Link('Go to home', href='/app/', target="_blank"))
        nav_links.append(html.Br())
                
        nav_div = html.Div(
            nav_links
        )
        
        return nav_div



        
