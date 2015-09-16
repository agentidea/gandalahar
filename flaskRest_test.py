import requests
url = 'http://www.agentidea.com:80/api/allegro/triple'

params = { 'repo':'doug',
           'ns':'rdf.agentidea.com',
           'sub':'agent/DougFinke',
           'pred':'spec/#term_knows',
           'obj':'agent/MarkBurgess'}

request = requests.Request('POST', url, data=params).prepare()
with requests.Session() as s:
    response = s.send(request,verify=False)

if response.status_code == 200:
    payload = response.json()
    print payload
else:
    print response
