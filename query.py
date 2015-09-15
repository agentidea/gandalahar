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

def __getTypedLiteral(conn, namespace, subjectLocalName, predicateLocalName, objLiteral=None, datatype="STRING"):
    exns = "http://%s/" % namespace
    subject_ = conn.createURI(namespace=exns, localname=subjectLocalName)
    predicate_ = conn.createURI(namespace=exns, localname=predicateLocalName)

    object_ = None
    if(objLiteral!=None):
        object_ = conn.createLiteral(objLiteral,__getDatatype(datatype))

    return subject_, predicate_, object_


def __getUUU(conn, namespace, subjectLocalName, predicateLocalName, objectLocalName):
    exns = "http://%s/" % namespace
    subject_ = conn.createURI(namespace=exns, localname=subjectLocalName)
    predicate_ = conn.createURI(namespace=exns, localname=predicateLocalName)
    object_ = conn.createURI(namespace=exns, localname=objectLocalName)

    return subject_, predicate_, object_


def addTripleUUU(targetRepo, subjectURI, predicateURI, objectURI):
    conn = getConn(targetRepo)

    subject_ = conn.createURI(subjectURI)
    predicate_ = conn.createURI(predicateURI)
    object_ = conn.createURI(objectURI)

    beforeCount = conn.size()
    conn.add(subject_,predicate_,object_)
    afterCount = conn.size()

    return afterCount-beforeCount


def existsTripleUUnsTyped(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,conn=None):

        if conn==None:
            conn = getConn(targetRepo)

        subject_, predicate_,object_ = __getTypedLiteral(conn,namespace,
                                                 subjectLocalName,
                                                 predicateLocalName)

        statements = conn.getStatements(subject_,predicate_,object_)

        numStatements = len(statements.string_tuples)
        #statements.enableDuplicateFilter() ## there are no duplicates, but this exercises the code that checks

        counter = 0
        for s in statements:
            print s
            counter = counter + 1


        if counter != numStatements:
            msg = "Error counter [{}] and numstatements [{}] out of sync".format( counter, numStatements)
            raise Exception(msg)

        statements.close()
        conn.close()

        return numStatements

def existsTripleUULnsTyped(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objLiteral,conn=None, datatype="STRING"):

        if conn==None:
            conn = getConn(targetRepo)

        subject_, predicate_,object_ = __getTypedLiteral(conn,namespace,
                                                 subjectLocalName,
                                                 predicateLocalName,
                                                 objLiteral,datatype)

        statements = conn.getStatements(subject_,predicate_,object_)

        numStatements = len(statements.string_tuples)
        #statements.enableDuplicateFilter() ## there are no duplicates, but this exercises the code that checks

        counter = 0
        for s in statements:
            print s
            counter = counter + 1

        if counter != numStatements:
            msg = "Error counter [{}] and numstatements [{}] out of sync".format( counter, numStatements)
            raise Exception(msg)

        statements.close()
        conn.close()

        return numStatements

def existsTripleUUU(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objectLocalName,conn=None):

        if conn==None:
            conn = getConn(targetRepo)

        subject_, predicate_,object_ = __getUUU(conn,namespace,
                                                 subjectLocalName,
                                                 predicateLocalName,
                                                 objectLocalName)

        statements = conn.getStatements(subject_, predicate_, object_)

        numStatements = len(statements.string_tuples)
        #statements.enableDuplicateFilter() ## there are no duplicates, but this exercises the code that checks

        counter = 0
        for s in statements:
            print s
            counter = counter + 1

        if counter != numStatements:
            msg = "Error counter [{}] and numstatements [{}] out of sync".format( counter, numStatements)
            raise Exception(msg)

        statements.close()
        conn.close()

        return numStatements

def addTripleUUUns(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objectLocalName, preventDuplicates = True):
    conn = getConn(targetRepo)

    subject_, predicate_,object_ = __getUUU(conn,namespace,
                                                 subjectLocalName,
                                                 predicateLocalName,
                                                 objectLocalName)
    numberAdded = 0

    if(preventDuplicates):
        if(existsTripleUUU(targetRepo,namespace,subjectLocalName,predicateLocalName,objectLocalName,conn)):
            print "exists, ignoring save"
            numberAdded = 0
        else:
            beforeCount = conn.size()
            conn.add(subject_, predicate_, object_)
            afterCount = conn.size()
            numberAdded = afterCount-beforeCount
    else:
        print "grok why allowing duplicate UUU triples is a good idea????"
    return numberAdded






def addTripleUULnsTyped(targetRepo, namespace,
                   subjectLocalName,
                   predicateLocalName,
                   objLiteral, datatype="STRING", preventDuplicates = True):
    conn = getConn(targetRepo)
    subject_, predicate_,object_ = __getTypedLiteral(conn,namespace,
                                                 subjectLocalName,
                                                 predicateLocalName,
                                                 objLiteral,datatype)

    numberAdded = 0

    if(preventDuplicates):
        print "check exists"
        if( existsTripleUULnsTyped(targetRepo,namespace,subjectLocalName,predicateLocalName,objLiteral,conn,datatype)):
            print "existed, no update"
            numberAdded = 1
        else:
            print "adding new ..."
            beforeCount = conn.size()
            conn.add(subject_, predicate_, object_)
            afterCount = conn.size()
            numberAdded = afterCount-beforeCount
    else:
        print "must still grok why dups should be allowed???"
    return numberAdded


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


def getTriples(targetRepo):
    conn = getConn(targetRepo)
    rez = []
    try:
        queryString = "SELECT ?s ?p ?o  WHERE {?s ?p ?o .}"
        tupleQuery = conn.prepareTupleQuery(QueryLanguage.SPARQL, queryString)
        result = tupleQuery.evaluate();
        try:
            for bindingSet in result:
                s = bindingSet.getValue("s")
                p = bindingSet.getValue("p")
                o = bindingSet.getValue("o")
                rez.append([s.getValue(), p.getValue(), o.getValue()])
        finally:
            result.close()
    finally:
        conn.close();
        return rez



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



def testE():

    ret = existsTripleUULnsTyped('scratch',
                     'rdf.agentidea.com',
                     'agents/GrantSteinfeld',
                     'spec/people/#term_age',
                     48,datatype="INT")

    print ret
    ret = addTripleUULnsTyped('scratch',
                         'rdf.agentidea.com',
                         'agents/GrantSteinfeld',
                         'spec/people/#term_age',
                         48,datatype="INT")



    print ret
    ret = existsTripleUULnsTyped('scratch',
                     'rdf.agentidea.com',
                     'agents/GrantSteinfeld',
                     'spec/people/#term_age',
                     48,datatype="INT")

    print ret

def testG():

    ret = existsTripleUUnsTyped('scratch',
                     'rdf.agentidea.com',
                     'agents/GrantSteinfeld',
                     'spec/people/#term_age')
    print ret

def testH():

    ret = addTripleUULnsTyped('scratch',
                         'rdf.agentidea.com',
                         'agents/GrantSteinfeld',
                         'spec/people/#term_age',
                         49,datatype="INT", preventDuplicates=True)
    print ret

def testI():

    ret = addTripleUUUns('scratch','rdf.agentidea.com','agents/GrantSteinfeld',
                         'spec/people/#term_barelyknows','agents/PaulSteinfeld')

    print ret





if __name__ == '__main__':

    #testI()
    #SNAR()
    print getTriples('scratch')

    # print getAttribute()
    # print getAttribute('HairColor')
    # print getAttributes()
    # rez = queryModel('bEBDD1E92x88', 'HairColor')
    # for r in rez:
    #     print r

