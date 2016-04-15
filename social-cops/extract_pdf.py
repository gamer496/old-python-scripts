import textract

def fun(path):
	try:
		filename=path+".pdf"
		text=textract.process(filename)
		f=open("ok.txt","w")
		f.write(text)
		f.close()
		return True
	except:
		return False

if __name__=="__main__":
	val=fun()
	if val==True:
		print "Success"
	else:
		print "Failed"