from flask import Flask
from flask.ext.restplus import Api, Resource
from flask.ext.cors import CORS
from query import *
import sys
import os.path
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,here)

srcPth = os.path.dirname(__file__)+'/src'
sys.path.append(srcPth)

app = Flask(__name__)
cors = CORS(app)
api = Api(app, version='1.0', title='Graph DB', description='REST API to AllegroGraph Triple Store')


@api.route('/model/<attribute>')
class Model(Resource):
    def get(self,attribute):
        return getAttribute(attribute)

    def post(self):
        api.abort(403)

@api.route('/models')
class Models(Resource):
    def get(self):
        return getAttributes()

    def post(self):
        api.abort(403)

@api.route('/story/<o>')
class Story(Resource):
    def get(self,o ):
        return getStory(o)

    def post(self):
        api.abort(403)


if __name__ == '__main__':
    app.run(host='agentidea.com', port=7878)
