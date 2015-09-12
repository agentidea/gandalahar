import json
from nltk.corpus import shakespeare
from xml.etree import ElementTree

def getPlayers():
    print "getPlayers"
    print dir(shakespeare)	
    print shakespeare.abspath()
    play = shakespeare.xml('dream.xml')
    title = ('%s: %s' % (play[0].tag, play[0].text))
    personae = [persona.text for persona in play.findall('PERSONAE/PERSONA')]
    return {'title':title,'personae':personae}

if __name__=='__main__':
    x= getPlayers()
    j = json.dumps(x)
    print j
