from selenium import webdriver
import extract_ids
import time
from pyvirtualdisplay import Display
import json
import threading
import csv
import io
import os


not_file=open("not_done.txt","w")

script_to_select_faizabad='''var e = document.getElementById("ddlDistricts");
var opts=e.options
for(var opt,j=0;j<opts.length,opt=opts[j];j++)
{
  if(opt.text=="Faizabad")
  {
    e.selectedIndex=j;
  }
}'''

script_to_input_id='''
var e=document.getElementById("txtEPICNo")
e.value='''

final_list=[]

def fun(url,ids,flag):



	display=Display(visible=0,size=(800,600))
	display.start()

	# selenium setup using firefox
	for id_element in ids:
		try:
			driver=webdriver.Firefox()
			driver.get(url)

			# manipulate the select button
			driver.execute_script(script_to_select_faizabad)

			# click the search button
			search_buttons=driver.find_elements_by_id("Button1")
			search_button=search_buttons[0]
			search_button.click()

			# input the id then click the search button again
			script_to_input_id_val=script_to_input_id+'''"'''+id_element+'''"'''
			driver.execute_script(script_to_input_id_val)
			search_buttons=driver.find_elements_by_id("Button1")
			search_button=search_buttons[0]
			search_button.click()

			# find the show link and go to that page
			all_links=driver.find_elements_by_tag_name("a")
			for link in all_links:
				if link.text=="Show":
					href_tag=link
			href_link=href_tag.get_attribute("href")
			driver.get(href_link)

			# initialize the dict and the values there

			element_dict={}

			# extracting candidate name
			element_dict["Name"]=driver.find_elements_by_id("lbl_NAME")[0].text

			# extracting fathers name
			element_dict["Fathers Name"]=driver.find_elements_by_id("lbl_RELATIVE_NAME")[0].text

			# extracting id
			element_dict["ID"]=driver.find_elements_by_id("lbl_EPIC")[0].text
			element_dict["Gender"]=driver.find_elements_by_id("lbl_SEX")[0].text

			# let's wrap it up
			print element_dict
			final_list.append(element_dict)
			driver.close()
		except:
			if flag:
				not_file.write(id_element+"\n")
			else:
				pass
	display.stop()



def run_drivers(url,path,ids,flag=True):

	some_list=[]
	k=ids.__len__()
	step=k/5

	threads=[]
	j=0

	for i in range(0,5):
		t=threading.Thread(target=fun,args=[url,ids[j:j+step],flag])
		j+=step
		threads.append(t)
		t.start()
		t.join()



def main_fun(url,path):
	ids=extract_ids.fun(path)
	run_drivers(url,path,ids)
	check_not_processed(url,path)
	end()



def check_not_processed(url,path):
	not_file.close()
	fil=open("not_done.txt","r")
	ids=[]
	for x in fil.readlines():
		x=x.rstrip("\n")
		ids.append(x)
	run_drivers(url,path,ids,False)

def end():
	# file_json.close()
	# not_file.close()
	with io.open("temp.txt","w",encoding="utf-8") as outfile:
		outfile.write(unicode(json.dumps(final_list,ensure_ascii=False)))
	with open("temp.txt") as infile:
		data=json.load(infile)
	with open("data.csv","w") as file:
		csv_file=csv.writer(file)
		for item in data:
			csv_file.writerow([item["ID"].encode('utf-8'),item["Name"].encode('utf-8'),item["Gender"].encode('utf-8'),item["Fathers Name"].encode('utf-8')])
	choice=raw_input("Remove temporary files?[yn]\n")
	if choice.lower()=='y':
		os.remove("temp.txt")
		os.remove("not_done.txt")


url="http://164.100.180.4/searchengine/SearchEngineEnglish.aspx"
path="ok"
main_fun(url,path)