__author__ = 'grantsteinfeld'
from datetime import datetime
from query import getTripleUU, addTripleUULnsTyped

def incrementForDay(apiCall):
    today = datetime.now()
    print type(today)
    key = "%s-%s" % (today.date(), apiCall)
    print key
    pred = 'spec/stats/#term_counter'

    ret = getTripleUU('stats','rdf.agentidea.com',key,pred)
    print ret


    # ret = addTripleUULnsTyped('stats',
    #                      'rdf.agentidea.com',
    #                      key,
    #                      'spec/stats/#term_counter',
    #                      15,"INT")
    #
    # print ret



if __name__ == '__main__':

    incrementForDay('alchemy')