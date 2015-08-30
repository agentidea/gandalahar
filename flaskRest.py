from flask import Flask
from flask.ext.restplus import Api, Resource
from flask.ext.cors import CORS
from query import *
from mailnewsparse import proc as getBreakingNews

import sys
import os.path
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,here)

srcPth = os.path.dirname(__file__)+'/src'
sys.path.append(srcPth)

app = Flask(__name__)
cors = CORS(app)
api = Api(app, version='0.1.22', title='AgentIdea API', description='REST API to various backend analytics and stores')


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


@api.route('/breakingnews')
class BreakingNews(Resource):
    def get(self):
	return getBreakingNews()
    def post(self):
	api.abort(403)

if __name__ == '__main__':
    app.run(host='agentidea.com', port=7878)
