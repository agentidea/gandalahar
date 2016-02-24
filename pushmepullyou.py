import requests
import json

urlNews = 'http://agentidea.com:80/api/news/breakingnews'
urlGet = 'https://hooks.slack.com/services/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'

def sendPayload(msg):
	payload = {
		"username":"pynewsbot",
		"text":msg,
		"icon_emoji": ":newspaper:"}
	payload = json.dumps(payload)

	r = requests.post(urlGet, data=payload)
	print r.status_code



col=[]
r = requests.get(urlNews)
data = r.json()
for d in data:
	if d['src'] != 'Facebook':
		if 'BREAKING' in d['subject']:
			sub = d['subject'].replace("BREAKING",'')
			sub = sub.replace("NEWS",'')
			sub = sub.replace(":",' ')
			sub = sub.strip()
			col.append(sub)
MAX=5
count=0 
for c in col:
	if count<MAX:
		sendPayload(c)
	count = count + 1
