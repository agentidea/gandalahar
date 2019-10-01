from flask import Flask, request, Response
from flask_restplus import Api, Resource, fields
from flask_cors import CORS
from query import *
from mailnewsparse import proc as getBreakingNews
from NorvigSpell import Spell
import sys
import os.path
from datetime import datetime
import pprint
from hamlet import getPlayers

from lookNews import Neo

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)


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

@allegroNS.route('/tripleLUU')
class TripleLUU(Resource):

    def post(self):
        '''
        post here default spo::Literal URI URI
        '''
        ret = 'not_set_yet'
        try:
            repo_ = request.form['repo']
            namespace_ = request.form['ns']
            subject_ = request.form['sub']
            predicate_ = request.form['pred']
            obj_ = request.form['obj']

            print obj_

            ret = addTripleLUUns(repo_,
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

@allegroNS.route('/tripleLUL')
class TripleLUL(Resource):

    def post(self):
        '''
        post here default spo::Literal URI Literal
        '''

        ret = 'not_set_yet'
        try:
            repo_ = request.form['repo']
            namespace_ = request.form['ns']
            subject_ = request.form['sub']
            predicate_ = request.form['pred']
            obj_ = request.form['obj']
            type_ = request.form['type']
            ret = addTripleLULnsTyped(repo_,
                         namespace_,
                         subject_,
                         predicate_,
                         obj_,
                         type_)

        except Exception as genex:
            api.abort(500, "ERROR: %s" % genex)

        return ret


@naturalLanguage.route('/play/<title>')
class Midsummer(Resource):
    def get(self,title):
        ret = None
        try:
            ret = getPlayers(title)
        except Exception as exp:
            ret = exp.message

        return ret

@naturalLanguage.route('/spellOne/<word>')
class SpellOne(Resource):
    def get(self, word):
        ret = None
        correct = True 
        try:
            spel = Spell()
            ret = spel.correct(word) 
            if ret != word:
                correct = False
	except Exception as spelex:
            ret = spelex

        return {"word":word, "corrected":ret, "correct":correct }

@naturalLanguage.route('/spellMany')
class SpellMany(Resource):
    def get(self, word):
        ret = None
        correct = True
        try:
            spel = Spell()
            ret = spel.correct(word)
            if ret != word:
                correct = False
        except Exception as spelex:
            ret = spelex

        return {"word":word, "corrected":ret, "correct":correct }

@humanNS.route('/model/<attribute>')
class Model(Resource):
    def get(self, attribute):
        if(attribute=='Text'): return {}
        return getAttribute(attribute)

    def post(self):
        api.abort(403)


@humanNS.route('/models')
class Models(Resource):
    def get(self):
        return getAttributes()

    def post(self):
        api.abort(403)


@newsNS.route('/src/<source>')
class Story(Resource):
    def get(self, source):
        return Neo().get_nodes_by_src(source)

@newsNS.route('/today/<daysBack>')
class NewsSpan(Resource):
    def get(self, daysBack):
        return Neo().get_nodes_back(int(daysBack))


@newsNS.route('/span/<start>/<end>')
class NewsSpan(Resource):
    def get(self, start, end):
        return Neo().get_nodes_span(int(start),int(end))

@newsNS.route('/breakingnews')
class BreakingNews(Resource):
    def get(self):
        return Neo().get_nodes() 


@debugNS.route('/tim/<code>')
class Tim(Resource):
    def get(self, code):
        timestamp_=str(datetime.now())
        if(int(code)==200 or int(code)==201):
            return "time is {}".format(timestamp_)
        else:
            api.abort(int(code))


@debugNS.route('/req')
class Reqq(Resource):
    def get(self):
        timestamp_=str(datetime.now())
        h = request.headers
        for h_ in h:
            print h_

	return 11












if __name__ == '__main__':
    #app.run(host='localhost', port=7878, debug=True)
    app.run(host='www.agentidea.com', port=7878)
