from flask import Flask, request, Response
from flask.ext.restplus import Api, Resource, fields
from flask.ext.cors import CORS
from query import *
from mailnewsparse import proc as getBreakingNews
from midsummer import getPlayers

import sys
import os.path
from datetime import datetime
import pprint

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)

srcPth = os.path.dirname(__file__) + '/src'
sys.path.append(srcPth)

app = Flask(__name__)
cors = CORS(app)
api = Api(app, version='0.1.24', title='AgentIdea API', description='REST API to various backend analytics and stores')

newsNS = api.namespace('news', 'news')
humanNS = api.namespace('human', 'models')
naturalLanguage = api.namespace('nlp', 'Natural Language Processing')
allegroNS = api.namespace('allegro', 'triple store operations')
debugNS = api.namespace('dbg', 'debugging calls')



@debugNS.route("/vars")
class Vars(Resource):
    def get():
        print "GETTING"
        str_ = pprint.pformat(request.environ, depth=5)
        print str_
        return Response(str_, mimetype="text/text")


#define the payload for pingpost
ping_post = api.model('PingPostResource', {
    'param1': fields.String,
    'param2': fields.Float
})

@debugNS.route('/pingpost')
class Pingpost(Resource):

    @api.expect(ping_post)
    def post(self):
        '''
        post test responds with what was passed up
        '''
        try:
            json_ = request.get_json()

            if 'param1' in json_ and 'param2' in json_:
                param1 = json_['param1']
                param2 = json_['param2']


                return [param1, param2, str(datetime.now())]
            else:
                raise Exception( "param1 and param2 are required")
        except Exception as genex:
            api.abort(500,genex.message)




@allegroNS.route('/triples/<repo>')
@api.doc(params={'repo':'repository name'})
class Triples(Resource):
    def get(self, repo):
        return getTriples(repo)


@allegroNS.route('/triple')
class Triple(Resource):

    def post(self):
        '''
        post here default spo::URI URI URI
        '''
        ret = 'not_set_yet'
        try:
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

        except Exception as genex:
            api.abort(500, "ERROR: %s" % genex)

        return ret


@allegroNS.route('/tripleUUL')
class TripleUUL(Resource):

    def post(self):
        '''
        post here default spo::URI URI Literal
        '''

        ret = 'not_set_yet'
        try:
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

        except Exception as genex:
            api.abort(500, "ERROR: %s" % genex)

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
    #app.run(host='localhost', port=7878, debug=True)
    app.run(host='www.agentidea.com', port=7878)
