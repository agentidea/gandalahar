import requests
url= 'http://localhost:7878/dbg/pingpost'

params = { 'param1':'Rhada' }

request = requests.Request('POST', url, data=params).prepare()
with requests.Session() as s:
    response = s.send(request,verify=False)

if response.status_code == 200:
    payload = response.json()
    print payload
else:
    print response