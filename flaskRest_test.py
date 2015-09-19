import requests
url = 'http://www.agentidea.com/api/allegro/triple'

params = { 'repo':'scratch',
           'ns':'rdf.agentidea.com',
           'sub':'agent/DougFinke',
           'pred':'spec/#term_knows',
           'obj':'agent/BatMan'}


request = requests.Request('POST', url, data=params).prepare()  # data could be json

print request.headers
print request.body

with requests.Session() as s:
    response = s.send(request,verify=False)




if response.status_code == 200:
    payload = response.json()
    print payload
else:
    print response
