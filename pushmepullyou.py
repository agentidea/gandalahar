import requests
import json

urlNews = 'http://agentidea.com:80/api/news/breakingnews'
urlGets =['https://hooks.slack.com/services/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','https://hooks.slack.com/services/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','https://hooks.slack.com/services/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']

def sendPayload(msg):
	payload = {
		"username":"pynewsbot",
		"text":msg,
		"icon_emoji": ":newspaper:"}
	payload = json.dumps(payload)
	for urlGet in urlGets:
		r = requests.post(urlGet, data=payload)
		print r.status_code



col=[]
r = requests.get(urlNews)
data = r.json()
for d in data:
	if d['subject'][1:2].lower() == 'hi' or d['subject'][1] == '?':
		continue
	if d['src'] != 'Facebook':
		sub = d['subject'].replace("BREAKING",'')
		sub = sub.replace("NEWS",'')
		sub = sub.replace(":",' ')
		sub = sub.strip()
		col.append(sub)

count=0 
for c in col:
	if count<6:
		sendPayload(c)
		print c
	count = count + 1
