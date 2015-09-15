from flask import Flask, request
from flask.ext.restplus import Api, Resource
from flask.ext.cors import CORS
from query import *
from mailnewsparse import proc as getBreakingNews

from nltk.corpus import shakespeare
from xml.etree import ElementTree
from midsummer import getPlayers

import sys
import os.path

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)

srcPth = os.path.dirname(__file__) + '/src'
sys.path.append(srcPth)

app = Flask(__name__)
cors = CORS(app)
api = Api(app, version='0.1.23', title='AgentIdea API', description='REST API to various backend analytics and stores')

newsNS = api.namespace('news', 'news')
humanNS = api.namespace('human', 'models')
naturalLanguage = api.namespace('nlp', 'Natural Language Processing')
allegroNS = api.namespace('allegro', 'triple store operations')


@allegroNS.route('/triples/<repo>')
class Triples(Resource):
    def get(self, repo):
        return getTriples(repo)


@allegroNS.route('/triple')
class Triple(Resource):

    def post(self):
        '''
        post here default spo::URI URI URI
        '''
        repo_ = request.form['repo']
        namespace_ = request.form['ns']
        subject_ = request.form['sub']
        predicate_ = request.form['pred']
        obj_ = request.form['obj']

        ret = addTripleUUUns(repo_,
                         namespace_,
                         subject_,
                         predicate_,
                         obj_)

        return ret

@allegroNS.route('/tripleUUL')
class TripleUUL(Resource):

    def post(self):
        '''
        post here default spo::URI URI Literal
        '''
        repo_ = request.form['repo']
        namespace_ = request.form['ns']
        subject_ = request.form['sub']
        predicate_ = request.form['pred']
        obj_ = request.form['obj']
        type_ = request.form['type']

        ret = addTripleUULnsTyped(repo_,
                         namespace_,
                         subject_,
                         predicate_,
                         obj_,
                         type_)

        return ret




@naturalLanguage.route('/midsummer')
class Midsummer(Resource):
    def get(self):
        ret = None
        try:
            ret = getPlayers()
        except Exception as exp:
            ret = exp.message

        return ret


@humanNS.route('/model/<attribute>')
class Model(Resource):
    def get(self, attribute):
        return getAttribute(attribute)

    def post(self):
        api.abort(403)


@humanNS.route('/models')
class Models(Resource):
    def get(self):
        return getAttributes()

    def post(self):
        api.abort(403)


@newsNS.route('/story/<o>')
class Story(Resource):
    def get(self, o):
        return getStory(o)

    def post(self):
        api.abort(403)


@newsNS.route('/breakingnews')
class BreakingNews(Resource):
    def get(self):
        return getBreakingNews()

    def post(self):
        api.abort(403)


if __name__ == '__main__':
    app.run(host='localhost', port=7878)
