import requests
url = 'http://localhost:7878/allegro/triple'

params = { 'repo':'scratch',
           'ns':'rdf.agentidea.com',
           'sub':'agent/GrantSteinfeld',
           'pred':'spec/#term_nick',
           'obj':'Gandalahar',
           'type':'STRING'}

request = requests.Request('POST', url, data=params).prepare()


with requests.Session() as s:
    response = s.send(request,verify=False)

if response.status_code == 200:
    payload = response.json()
    print payload
else:
    print response
