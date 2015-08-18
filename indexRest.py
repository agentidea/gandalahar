import sys
import os.path
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,here)

srcPth = os.path.dirname(__file__)+'/src'
sys.path.append(srcPth)
from src import app


app.config['APPLICATION_ROOT'] = '/baroness/'

def application(environ, start_response):
    #sys.path.append('/opt/pycharm-4.0.6/debug-eggs/pycharm-debug.egg')
    #import pydevd
    #pydevd.settrace('localhost', port=5555, stdoutToServer=True, stderrToServer=True)
    #capture every request coming in ...
    app.logger.debug("environ %s" % environ)
    return app(environ, start_response)
