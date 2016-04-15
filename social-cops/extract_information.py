from selenium import webdriver
import extract_ids
import time
from pyvirtualdisplay import Display
import json
import threading


file_json=open("temp.txt","w")

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

def fun(url,ids):



	display=Display(visible=0,size=(800,600))
	display.start()

	# selenium setup using firefox
	for id_element in ids:
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
		info=json.dumps(element_dict)
		file_json.write(info+"\n")
		driver.close()
	display.stop()



def run_drivers(url,path):

	some_list=[]
	ids=extract_ids.fun(path)
	k=ids.__len__()
	k=10
	step=k/5

	threads=[]
	j=0

	for i in range(0,5):
		t=threading.Thread(target=fun,args=[url,ids[j:j+step]])
		j+=step
		threads.append(t)
		t.start()
	return some_list




if __name__=="__main__":
	url="http://164.100.180.4/searchengine/SearchEngineEnglish.aspx"
	path="ok"
	run_drivers(url,path)