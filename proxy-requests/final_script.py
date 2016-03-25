from selenium import webdriver
import selenium.webdriver.support.ui as ui
import urllib
import requests
import time
from pyvirtualdisplay import Display

def setup():
    fp=webdriver.FirefoxProfile()
    fp.set_preference("http.response.timeout",60)
    fp.set_preference("dom.max_script_run_time",60)
    driver=webdriver.Firefox(firefox_profile=fp)
    driver.set_page_load_timeout(60)
    driver.set_script_timeout(60)
    return driver

def setup_proxy(ip,port):
	fp=webdriver.FirefoxProfile()
	fp.set_preference("network.proxy.type", 1)
	fp.set_preference("network.proxy.http",ip)
	fp.set_preference("network.proxy.http_port",int(port))
	fp.set_preference("http.response.timeout",60)
	fp.set_preference("dom.max_script_run_time",60)
	driver=webdriver.Firefox(firefox_profile=fp)
	driver.set_page_load_timeout(60)
	driver.set_script_timeout(60)
	return driver

display=Display(visible=0,size=(800,600))
display.start()
pros=[]
driver=setup()
for i in range(1,11):
    url="https://proxy-list.org/english/index.php?p="+str(i)
    driver.get(url)
    k=driver.find_elements_by_xpath("//li[@class='proxy']")
    for x in k[1:]:
        pros.append(x.text)
driver.close()
url=raw_input("Enter the url:\n")
for proxy in pros:
	print proxy.split(":")
	try:
		ip,port=proxy.split(":")
		driver=setup_proxy(ip,port)
		driver.get(url)
		wait=ui.WebDriverWait(driver,150).until(lambda driver:driver.find_element_by_id("fullresponsivefacebookpagelikeclose").is_displayed())
		k=driver.find_elements_by_id("fullresponsivefacebookpagelikeclose")
		k[0].click()
		for i in range(0,4):
			driver.execute_script("window.scrollTo(0,700)")
			time.sleep(2)
		driver.close()
	except:
		print "bc"
		if driver:
			driver.close()
display.stop()