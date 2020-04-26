import os,datetime
from db import dbop, imgpath,hash
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,hash(password),email,phonenum,s,birthday),False)
def uploadimage(image:list,id,des):
    path=os.path.join(imgpath,des,str(id))
    if not os.path.exists(path):
        os.makedirs(path)
    for t,n in zip(image,range(0,len(image))):
        finalpath=os.path.join(path,des+str(id)+str(n)+'.'+t.filename.split('.')[-1])
        if not os.path.exists(finalpath):
            a=open(finalpath,'w')
            a.close()
        t.save(finalpath)
def uploadavatar(image,id):
    rmavatar(image[0],id)
    uploadimage(image,id,'avatar')
def uploaditemimg(image,itemid):
    uploadimage(image,id,'items')
def uploadalbum(image,id):   
    uploadimage(image,id,'album')
def delimage(image,id,des,seq):
    path=os.path.join(imgpath,des,str(id))
    if os.path.exists(path):
        finalpath=os.path.join(path,des+str(id)+str(seq)+'.'+image.filename.split('.')[-1])
        if os.path.exists(finalpath):
            os.remove(finalpath)
def rmavatar(image,id):
    delimage(image,id,'avatar',1)
