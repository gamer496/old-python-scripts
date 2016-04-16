import extract_pdf
import os

def fun(path):
	try:
		extract_pdf.fun(path)
		f=open("ok.txt","r")
		ids=[]
		for line in f.readlines():
			line=line.rstrip("\n")
			if line.isalnum() and line.__len__()>6:
				ids.append(line)
		os.remove(path+".txt")
		return ids
	except:
		return None

if __name__=="__main__":
	l=fun("ok")