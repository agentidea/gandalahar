from datetime import datetime, timedelta
from py2neo import Graph
from py2neo import cypher
from pandas import DataFrame
import logging
logger = logging.Logger(__name__)

class Neo():
    def __init__(self, hostname='localhost',  password='jy1met2'):
        self.host = hostname
        self.password = password

    def get_nodes(self, daysBack=None):
        if daysBack is not None:
            dateString = self.getDateBack(daysBack)
            query = "MATCH (n:Article) WHERE n.Date > '{}' RETURN n.From, n.Subject, n.Date".format(dateString)
        else:
            query = "MATCH (n:Article) RETURN n.From, n.Subject, n.Date"
        print query 
        graph = Graph(password=self.password)
        df = DataFrame(graph.data(query))
        d = df.to_dict()
        rez = []

        for k, v in d['n.Subject'].items():
            subject = v
            date = d['n.Date'][k]
            rez.append({ 'date': date, 'subject':subject})
        
        return rez


    def getDateBack(self, daysBack):
        date_N_days_ago = datetime.now() - timedelta(days=int(daysBack))
        return str(date_N_days_ago).split(' ')[0]
