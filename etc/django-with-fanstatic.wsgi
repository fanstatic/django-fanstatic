#!/opt/local/Library/Frameworks/Python.framework/Versions/2.6/Resources/Python.app/Contents/MacOS/Python


import sys
sys.path[0:0] = [
  '/Users/shanx/project/django-fanstatic/src',
    '/Users/shanx/project/django-fanstatic/testing',
    '/Users/shanx/project/django-fanstatic/eggs/pudb-2011.1-py2.6.egg',
    '/Users/shanx/project/django-fanstatic/eggs/djangorecipe-0.20-py2.6.egg',
    '/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages',
    '/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages',
    '/Users/shanx/project/django-fanstatic/eggs/zc.buildout-1.5.2-py2.6.egg',
    '/Users/shanx/project/django-fanstatic/eggs/urwid-0.9.9.1-py2.6-macosx-10.6-x86_64.egg',
    '/Users/shanx/project/django-fanstatic/parts/django',
    '/Users/shanx/project/django-fanstatic/src/fanstatic',
    '/Users/shanx/project/django-fanstatic/eggs/setuptools-0.6c12dev_r88795-py2.6.egg',
    '/Users/shanx/project/django-fanstatic/eggs/WebOb-1.0.5-py2.6.egg',
    '/Users/shanx/project/django-fanstatic/eggs/Paste-1.7.5.1-py2.6.egg',
    '/Users/shanx/project/django-fanstatic/parts/django',
    '/Users/shanx/project/django-fanstatic',
  ]

import djangorecipe.wsgi
from django_fanstatic.handlers import FanstaticWSGIHandler

application = FanstaticWSGIHandler(djangorecipe.wsgi.main('testproject.settings', logfile=''))
