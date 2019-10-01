from __future__ import print_function
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

    def get_day_of_year(self):
        date_ = datetime.now()
        return date_.timetuple().tm_yday

    def get_nodes(self, daysBack=None):
        """ get nodes """

        if daysBack is not None:
            raise NotImplementedError("days back is not an option")

        rez_today = self.get_nodes_back(daysBack = 0)
        rez_yesterday = self.get_nodes_back(daysBack = 1)

        return rez_yesterday + rez_today

    def get_nodes_span(self, start, end):
        start = int(start)
        end = int(end)

        if start > end:
            raise Exception("start must be less than end")

        rez = []
        for i in range(start, end):
            try:
                x= self.get_nodes_back(daysBack = i)
                rez.append(x)
            except:
                continue

        return rez

    def get_nodes_back(self, daysBack):
        day_of_year = int(self.get_day_of_year()) - daysBack
        query = "MATCH (n) WHERE (n.day_of_year={} AND n.`x-src-param` IS NOT NULL) RETURN n.Subject, n.day_of_year,  n.short_date, n.FromEmail, n.`x-src-param`".format(day_of_year)
        graph = Graph(password=self.password)
        df = DataFrame(graph.data(query))
        d = df.to_dict()
        rez = []
        for k, v in d['n.Subject'].items():
            subject = v
            date = d['n.short_date'][k]
            _day_of_year= d['n.day_of_year'][k]
            _from = d['n.FromEmail'][k]
            _src = d['n.`x-src-param`'][k]
            _body = d['n.Body'][k]
            rez.append({ 'day_of_year': _day_of_year, 'date': date, 'src': _src, 'subject':subject, 'from':_from, 'body':_body})
        
        return rez


    def getDateBack(self, daysBack):
        date_N_days_ago = datetime.now() - timedelta(days=int(daysBack))
        return str(date_N_days_ago).split(' ')[0]




    def get_nodes_by_src(self, src):
        #query = "MATCH (n) WHERE ( n.`x-src-param` IS NOT NULL AND n.`x-src-param`=\"{}\" AND n.Body IS NOT NULL) RETURN n.Subject, n.day_of_year,  n.short_date, n.FromEmail, n.`x-src-param`, n.Body".format(src)
        query = "MATCH (n) WHERE ( n.`x-src-param` IS NOT NULL AND n.`x-src-param`=\"{}\" ) RETURN n.Subject, n.day_of_year,  n.short_date, n.FromEmail, n.`x-src-param`".format(src)
        print(query)
        graph = Graph(password=self.password)
        df = DataFrame(graph.data(query))
        d = df.to_dict()
        rez = []
        try:
            for k, v in d['n.Subject'].items():
                subject = v
                date = d['n.short_date'][k]
                _day_of_year= d['n.day_of_year'][k]
                _from = d['n.FromEmail'][k]
                _src = d['n.`x-src-param`'][k]
                rez.append({ 'day_of_year': _day_of_year, 'date': date, 'src': _src, 'subject':subject, 'from':_from})
        except:
            pass

        return rez




if __name__ == '__main__':
    z = Neo()
    n = z.get_nodes_by_src("blockchain")
    #n = z.get_nodes()
    #n = z.get_nodes_span(1,5)
    print(n) 
