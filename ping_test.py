import requests
url= 'http://www.agentidea.com:80/api/debug/pingpost'

params = { 'param1':'Rhada',
           'param2':'Puppy'}

request = requests.Request('POST', url, data=params).prepare()
with requests.Session() as s:
    response = s.send(request,verify=False)

if response.status_code == 200:
    payload = response.json()
    print payload
else:
    print response