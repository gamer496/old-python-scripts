import smtplib
file=raw_input("enter the filename:\n")
l=[]
# d={}
# d["type"]=raw_input("enter type:\n")
# d["product"]=raw_input("enter product:\n")
# d["position"]=raw_input("enter position:\n")
l=[]
with open(file,"r") as f:
    for line in f:
        for word in line.split(" "):
            # if word[0]=="{":
            #     if word[1]=="{":
            #         print word
            #         le=word.__len__()
            #         word=word[2:le-2]
            #         word=d[word]
            #         print word
            l.append(word)
s=""
s+=" "
for x in l:
    if x=="\n":
        s+=x
    else:
        s=s+x+" "
sender="singhjasdeep496@gmail.com"
receiver=raw_input("Enter the recepient:\n")
msg="\r\n".join([
    "From: "+sender,
    "To: "+receiver,
    "Subject: Intern Application",
    "",
    s
    ])
username="singhjasdeep496@gmail.com"
password="xyzzy@&$88008010"
server=smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(sender,[receiver],msg)
server.quit()
