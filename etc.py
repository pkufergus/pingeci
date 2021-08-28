# -*- coding: UTF-8 -*-

import os.path, sys, time

etc = {}

etc['debug'] = True
etc['error'] = False
etc['servs'] = 'AL/1.0.%s' % int(time.time())

etc['root_path'] = sys.path[0]
etc['login_url'] = '/login'
etc['xsrf_cookies'] = True
etc['cookie_secret'] = 'Yoursecretcookie'
etc['template_path'] = os.path.join(etc['root_path'], 'templates', '')
etc['database_path'] = os.path.join(etc['root_path'], 'data', '')
etc['static_path'] = 'www'
etc['static_url_prefix'] = '/www/'

settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'static_url_prefix': '/static/',
}