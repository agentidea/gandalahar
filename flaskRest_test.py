import requests
url = 'http://www.agentidea.com/api/allegro/tripleLUU'

params = { 'repo':'scratch',
           'ns':'rdf.agentidea.com',
           'sub':'xyz',
           'pred':'spec/#term_src',
           'obj':'http://finked.com/home/new.aspx'}


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
