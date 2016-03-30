from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import requests
import sys
import os


def download_file(pa,url):
	try:
		local_filename=url.split("/")[-1]
		r=requests.get(url,stream=True)
		curr_size=0
		with open(os.path.join(pa,local_filename),"wb") as f:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
					curr_size+=1024
					print "downloaded "+str(curr_size)+"		\r",
		return local_filename
	except:
		print "error downloading video"
		return None


base_url="http://ancensored.com"
query=raw_input("Enter the name of movie,celeb or tv show:\n")


try:
	query=query.split()
	for i in range(0,query.__len__()):
		query[i]=query[i][0].upper()+query[i][1:]
except:
	print "some error in splitting"
	sys.exit()


try:
	type=raw_input("options:\n[1] Celebrity\n[2] tv-show\n[3] movie\n")
	if type=="1":
		type="celebrities"
	elif type=="2":
		type="tv-shows"
	else:
		type="movies"
except:
	print "error in type handling."
	sys.exit()


try:
	fquery=''
	for quer in query:
		fquery=fquery+quer+'-'
	fquery=fquery[:-1]
except:
	print "some error in query conversion."
	sys.exit()


try:
	url=base_url+"/"+type+"/"+fquery
	soup=BeautifulSoup(urlopen(url))
except:
	print "Looks like you don't have the required packages.Please note the requirements.txt"


try:
	atags=soup.findAll("a",{"class":"button green"})
	links=[]
	for atag in atags:
		if not atag.has_key('href'):
			continue
		links.append(atag['href'])
except:
	print "relevant tags could not be scraped."
	sys.exit()


try:
	vlinks=[]
	for link in links:
		url=base_url+link
		soup=BeautifulSoup(urlopen(url))
		texts=soup.findAll("font",{"size":"3"})
		flag=False
		for text in texts:
			if text.text.__contains__("Current nudity level of this appearance"): #and text.text.__contains__("Nude"):
				flag=True
		if flag==False:
			continue
		atags=soup.findAll("a")
		for atag in atags:
			if atag.has_key("href") and atag["href"].__contains__("/clip") and atag["href"].__contains__(fquery) and not atag["href"].__contains__("comments"):
				vlinks.append(atag["href"])
except:
	print "couldn't find video urls"


try:
	fvlinks=[]
	for vlink in vlinks:
		url=base_url+vlink
		soup=BeautifulSoup(urlopen(url))
		atags=soup.findAll("a",{"id":"player"})
		for atag in atags:
			fvlinks.append(atag['href'])
except:
	print "some problem occurred in video links scraping."


try:
	option=raw_input("a totel of "+str(len(fvlinks))+" videos will be downloaded.Continue?[yn]\n")
	flag=True
	while flag==True:
		if option.lower()!='y' and option.lower()!='n':
			option=raw_input("Please enter y or n\n")
		else:
			flag=False
	if option.lower()=="n":
		sys.exit()
except:
	print "some error occurred.Cannot proceed."
	sys.exit()


try:
	i=1
	pa=raw_input("enter the path wherein to save the vids\n")
	flag=False
	while flag==False:
		if not os.path.exists(pa):
			pa=raw_input("no such path exists enter again\n")
		else:
			flag=True
except:
	print "some internal problem occurred."
	sys.exit()


for fvlink in fvlinks:
	try:
		url=base_url+"/"+fvlink
		print "downloading video number "+str(i)
		name=download_file(pa,url)
		if name:
			print "saved in "+name
	except:
		print "error in video number "+str(i)
	i+=1