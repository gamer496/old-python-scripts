import os

i=0
def fun(pa):
	for x in os.listdir(pa):
		if os.path.isdir(os.path.join(pa,x)):
			fun(os.path.join(pa,x))
		else:
			fn,fe=os.path.splitext(x)
			na=fn+str(i)+".mp3"
			pas=os.path.join(sap,na)
			print os.path.join(pa,x)
			choice=raw_input("Convert "+x+" in mp3 format:\n")
			if choice.lower()=="yes" or choice.lower()=="y":
				command='ffmpeg -i ' + '"' +os.path.join(pa,x)+ '"' + ' -acodec libmp3lame ' + '"' + pas + '"'
				os.system(command)
			else:
				print "Not converting "+x+" moving onto next."
			i+=1
sap="/media/gamer496/63CAB60D476EDFB2/portmu"
fun(os.getcwd())
print i