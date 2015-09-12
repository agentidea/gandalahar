import sys
import os.path
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,here)
srcPth = os.path.dirname(__file__) + '/src'
sys.path.append(srcPth)
from flaskRest import app
corpi = "/home/agentidea/nltk_data/corpora"
sys.path.append(corpi)

app.config['APPLICATION_ROOT'] = '/api/'

def application(environ, start_response):
    return app(environ, start_response)
