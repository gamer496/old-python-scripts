from BeautifulSoup import BeautifulSoup
import requests
from selenium import webdriver
from pyvirtualdisplay import Display
import json


f=open("log.txt","w")
main_file=open("results.txt","w")
pen_list=[]


def parse_to_proper(lis):
	return {v["link"]:v for v in l}.values()

def parse_link(link,text,appen):
	if link[-1]=="/":
		link=link[:-1]
	return link+"/"+text+"/"+appen+"/"


def extract_main(link):
	try:
		main_soup=BeautifulSoup(requests.get(link).content)
	except:
		f.write("main soup couldn't be extracted.")
	d={}
	d["link"]=link
	try:
		d["title"]=main_soup.find("h1",{"class":"entry-title"}).text
	except:
		d["title"]=" "
		f.write("for link "+link+" title couldn't be parsed")
	try:
		driver=webdriver.Firefox()
		driver.get(link)
		boxes=driver.find_elements_by_id("rating_box")
		box=boxes[0]
		d["rating"]=box.text
	except:
		d["rating"]=0
		f.write("problem for link "+link+" couldn't extract rating.\n")
	if d["rating"]==0:
		d["rating"]=6
	pen_list.append(d)
	print d



def extract_links(page_soup):
	all_main_links=page_soup.findAll("a",{"rel":"bookmark"})
	links=[]
	for link in all_main_links:
		try:
			links.append(link["href"])
		except:
			f.write("could not extract main link\n")
	for link in links:
		try:
			extract_main(link)
		except:
			f.write("problem in calling extract main.")


def has_link(page_soup):
	pagi_link=page_soup.findAll("a",{"class":"nextpostslink"})
	if len(pagi_link)>=1:
		return True
	else:
		return False

def paginatable(url):
	display=Display(visible=0,size=(800,600))
	display.start()
	all_pagi=[]
	try:
		page_soup=BeautifulSoup(requests.get(url).content,convertEntities=BeautifulSoup.HTML_ENTITIES)
		i=1
	except:
		f.write("could not extract page soup\n")
	while has_link(page_soup):
		try:
			extract_links(page_soup)
			i+=1
			url=parse_link(url,"page",str(i))
			page_soup=BeautifulSoup(requests.get(url).content,convertEntities=BeautifulSoup.HTML_ENTITIES)
		except:
			f.write("some problem in page extraction logic\n")
	display.stop()

base_url="http://www.geeksforgeeks.org/"
home_soup=BeautifulSoup(requests.get(base_url).content,convertEntities=BeautifulSoup.HTML_ENTITIES)

all_categories=[]
options=home_soup.findAll("option")
for option in options:
	try:
		txt=option.text
		txt='-'.join(txt.split()[:-1])
		txt=txt.lower()
		all_categories.append(txt)
	except:
		f.write("problem in category extraction.\n")


for category in all_categories:
	paginatable(parse_link(base_url,"category/",category))

pen_list=parse_to_proper(pen_list)

for x in pen_list:
	print x["link"]
	main_file.write(json.dumps(x))
f.close()
main_file.close()