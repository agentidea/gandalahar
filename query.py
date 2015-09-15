from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
from franz.openrdf.vocabulary.xmlschema import XMLSchema
from franz.openrdf.rio.rdfformat import RDFFormat
import os

CURRENT_DIRECTORY = os.getcwd() 

AG_HOST = os.environ.get('AGRAPH_HOST', 'www.agentidea.com')
AG_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AG_CATALOG = ''
AG_USER = 'allegroadmin'
AG_PASSWORD = 'kingfisher'

def __getDatatype(stringType):
    if stringType.upper() == "INT":
        return XMLSchema.INT
    if stringType.upper() == "LONG":
        return XMLSchema.LONG
    if stringType.upper() == "DOUBLE":
        return XMLSchema.DOUBLE
    if stringType.upper() == "DECIMAL":
        return XMLSchema.DECIMAL
    if stringType.upper() == "FLOAT":
        return XMLSchema.FLOAT
    if stringType.upper() == "STRING":
        return XMLSchema.STRING
    if stringType.upper() == "BOOLEAN":
        return XMLSchema.BOOLEAN

    raise Exception("Unhandled Type %s" % stringType)

def getConn(repo='baroness', accessMode=Repository.OPEN):

    server = AllegroGraphServer(AG_HOST, AG_PORT, AG_USER, AG_PASSWORD)
    catalog = server.openCatalog()
    myRepository = catalog.getRepository(repo, accessMode)
    myRepository.initialize()
    conn = myRepository.getConnection()
    return conn


def addTripleUUU(targetRepo, subjectURI, predicateURI, objectURI):
    conn = getConn(targetRepo)

    subject_ = conn.createURI(subjectURI)
    predicate_ = conn.createURI(predicateURI)
    object_ = conn.createURI(objectURI)

    beforeCount = conn.size()
    conn.add(subject_,predicate_,object_)
    afterCount = conn.size()

    return afterCount-beforeCount

def addTripleUUUns(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objLocalName):
    conn = getConn(targetRepo)

    exns = "http://%s/" % namespace
    subject_ = conn.createURI(namespace=exns, localname=subjectLocalName)
    predicate_ = conn.createURI(namespace=exns, localname=predicateLocalName)
    object_ = conn.createURI(namespace=exns, localname=objLocalName)

    beforeCount = conn.size()
    conn.add(subject_, predicate_, object_)
    afterCount = conn.size()

    return afterCount-beforeCount


def addTripleUULns(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objLiteral):
    conn = getConn(targetRepo)

    exns = "http://%s/" % namespace
    subject_ = conn.createURI(namespace=exns, localname=subjectLocalName)
    predicate_ = conn.createURI(namespace=exns, localname=predicateLocalName)
    object_ = conn.createLiteral(objLiteral)

    beforeCount = conn.size()
    conn.add(subject_, predicate_, object_)
    afterCount = conn.size()

    return afterCount-beforeCount

def addTripleUULnsTyped(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objLiteral, datatype="INT"):
    conn = getConn(targetRepo)
    datatype_ = __getDatatype(datatype)

    exns = "http://%s/" % namespace
    subject_ = conn.createURI(namespace=exns, localname=subjectLocalName)
    predicate_ = conn.createURI(namespace=exns, localname=predicateLocalName)
    object_ = conn.createLiteral(objLiteral, datatype_)

    beforeCount = conn.size()
    conn.add(subject_, predicate_, object_)
    afterCount = conn.size()

    return afterCount-beforeCount


def addTripleUUL(targetRepo, subjectURI, predicateURI, objLiteral):
    conn = getConn(targetRepo)

    subject_ = conn.createURI(subjectURI)
    predicate_ = conn.createURI(predicateURI)
    object_ = conn.createLiteral(objLiteral)

    beforeCount = conn.size()
    conn.add(subject_,predicate_,object_)
    afterCount = conn.size()

    return afterCount-beforeCount



def addTripleTypedObj(targetRepo, subjectURI, predicateURI, objLiteral, datatype="INT"):
    conn = getConn(targetRepo)
    datatype_ = __getDatatype(datatype)

    subject_ = conn.createURI(subjectURI)
    predicate_ = conn.createURI(predicateURI)
    object_ = conn.createLiteral(objLiteral, datatype_)

    beforeCount = conn.size()
    conn.add(subject_,predicate_,object_)
    afterCount = conn.size()

    return afterCount-beforeCount




def loadRDF(targetRepo, path1 = "./rdfUpload/python-lesmis.rdf" ):
    conn = getConn(targetRepo)
    conn.addFile(path1, None, format=RDFFormat.RDFXML);


def queryModel(anonKey, predicateSuffix='EyeColor'):
    conn = getConn()
    queryString = """
    SELECT ?o
    {
        _:%s <http://rdf.agentidea.com/personals/%s> ?o.
    }
    """ % (anonKey, predicateSuffix)

    print queryString
    tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
    result = tupleQuery.evaluate()

    rez = []
    counter = 0
    for bindingSet in result:
       rez.append({'seq': counter,
                   'predSuffix':predicateSuffix,
                   'id': anonKey,
                   'o':bindingSet.getValue('o').getValue().strip()
                  })
       counter = counter + 1

    return rez




def	getAttribute(predicateSuffix='EyeColor'):
    conn = getConn()
    queryString = """
    SELECT ?s ?o
    {
        ?s <http://rdf.agentidea.com/personals/%s> ?o.
    }
    """ % predicateSuffix

    tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
    result = tupleQuery.evaluate()

    rez = []
    counter = 0
    for bindingSet in result:
       rez.append({'seq': counter,
                   's': bindingSet.getValue('s').getValue().strip(),
                   'o':bindingSet.getValue('o').getValue().strip()
                  })
       counter = counter + 1

    return rez

def getStory(predicateSuffix='headline'):
    conn = getConn("Annie")
    queryString = """
    SELECT ?s ?o ?url
    {
        ?s <http://rdf.agentidea.com/%s> ?o.
        ?s <http://rdf.agentidea.com/url> ?url.
    }
    """ % predicateSuffix

    tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
    result = tupleQuery.evaluate()

    rez = []
    counter = 0
    for bindingSet in result:
       rez.append({'seq': counter,
                   's': bindingSet.getValue('s').getValue().strip(),
                   'url': bindingSet.getValue('url').getValue().strip(),
                   'o':bindingSet.getValue('o').getValue().strip()
                  })
       counter = counter + 1

    return rez

def getAttributes():
    conn = getConn()
    queryString= """
    select ?s ?eyeColor ?hairColor ?cup ?bust ?build ?age
    {
    ?s <http://rdf.agentidea.com/personals/EyeColor> ?eyeColor.
    ?s <http://rdf.agentidea.com/personals/HairColor> ?hairColor.
    ?s <http://rdf.agentidea.com/personals/Bust> ?bust.
    ?s <http://rdf.agentidea.com/personals/Cup> ?cup.
    ?s <http://rdf.agentidea.com/personals/Build> ?build.
    ?s <http://rdf.agentidea.com/personals/Age> ?age.
    }
    """
    tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
    result = tupleQuery.evaluate()
    rez = []
    for bindingSet in result:

        rez.append({'cup':bindingSet.getValue('cup').getValue().strip(),
        'eyeColor':bindingSet.getValue('eyeColor').getValue().strip(),
        'hairColor':bindingSet.getValue('hairColor').getValue().strip(),
        'bust':bindingSet.getValue('bust').getValue().strip(),
        'cup':bindingSet.getValue('cup').getValue().strip(),
        'build':bindingSet.getValue('build').getValue().strip(),
        'age':bindingSet.getValue('age').getValue().strip(),
        'id':bindingSet.getValue('s').getValue().strip()


    })
    return rez






def testA():

    ret = addTripleUUU("scratch", "http://rdf.agentidea.com/name/GrantSteinfeld",
                       "http://http://xmlns.com/foaf/spec/#term_knows",
                       "http://rdf.agentidea.com/name/LouiseSteinfeld")

    print ret


    ret = addTripleUUL("scratch", "http://rdf.agentidea.com/name/GrantSteinfeld",
                       "http://http://xmlns.com/foaf/spec/#term_knows",
                       "LouiseSteinfeld")

    print ret

    ret = addTripleTypedObj("scratch", "http://rdf.agentidea.com/name/GrantSteinfeld",
                       "http://xmlns.com/foaf/spec/#term_age",
                       42)

    print ret

    ret = addTripleTypedObj("scratch", "http://rdf.agentidea.com/name/GrantSteinfeld",
                       "http://xmlns.com/foaf/spec/#term_status",
                       "Ebullient and Pensive","string")

    print ret

def testB():
    ret = addTripleUULns('scratch',
                         'rdf.agentidea.com',
                         'agents/GrantSteinfeld',
                         'spec/people/#term_nick',
                         'Thor')

    print ret
    ret = addTripleUULns('scratch',
                         'rdf.agentidea.com',
                         'agents/GrantSteinfeld',
                         'spec/people/#term_foaf',
                         'agents/RhadaPuppy')

    print ret
    ret = addTripleUULns('scratch',
                         'rdf.agentidea.com',
                         'agents/RhadaPuppy',
                         'spec/people/#term_foaf',
                         'agents/GrantSteinfeld')
    print ret
    ret = addTripleUULns('scratch',
                         'rdf.agentidea.com',
                         'agents/RhadaPuppy',
                         'spec/people/#term_nick',
                         'Snorf')



    print ret
    ret = addTripleUULnsTyped('scratch',
                         'rdf.agentidea.com',
                         'agents/RhadaPuppy',
                         'spec/people/#term_age',
                         15,"INT")

    print ret

    ret = addTripleUULnsTyped('scratch',
                         'rdf.agentidea.com',
                         'agents/GrantSteinfeld',
                         'spec/people/#term_age',
                         48,"INT")

    print ret



def testD():
    bnode = addTripleBlankNode('scratch','http://rdf.agentidea.com/rel/A','foo','NumeroDuo')
    addTripleBlankNode('scratch','http://rdf.agentidea.com/rel/B','boo',bnode)
    addTripleBlankNode('scratch','http://rdf.agentidea.com/rel/N','noo',bnode)

if __name__ == '__main__':

    testB()
    #SNAR()


    # print getAttribute()
    # print getAttribute('HairColor')
    # print getAttributes()
    # rez = queryModel('bEBDD1E92x88', 'HairColor')
    # for r in rez:
    #     print r

