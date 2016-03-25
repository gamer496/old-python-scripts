import requests

msg=raw_input("Enter a message:\n")
phoneno=raw_input("Enter a phoneno:\n")

data={'number':phoneno,'message':msg}

r=requests.post("http://textbelt.com/text",data=data)

if r.json().has_key('success'):
	print "msg sent successfully"
else:
	print "some problem"