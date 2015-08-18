from franz.openrdf.sail.allegrographserver import AllegroGraphServer
from franz.openrdf.repository.repository import Repository
from franz.openrdf.query.query import QueryLanguage
import os

CURRENT_DIRECTORY = os.getcwd() 

AG_HOST = os.environ.get('AGRAPH_HOST', 'www.agentidea.com')
AG_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AG_CATALOG = ''
AG_USER = 'allegroadmin'
AG_PASSWORD = 'kingfisher'



def getConn(repo='baroness', accessMode=Repository.OPEN):

    server = AllegroGraphServer(AG_HOST, AG_PORT, AG_USER, AG_PASSWORD)
    catalog = server.openCatalog()
    myRepository = catalog.getRepository(repo, accessMode)
    myRepository.initialize()
    conn = myRepository.getConnection()
    return conn


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



#if __name__ == '__main__':

    #print getAttribute()
    #print getAttribute('HairColor')
    #print getAttributes()
    # rez = queryModel('bEBDD1E92x88', 'HairColor')
    # for r in rez:
    #     print r

