import hashlib
import os,datetime
from db import imgpath
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    r=hashlib.md5()
    r.update(password.encode(encoding='UTF-8'))
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    return 'insert into users (id,name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,r.hexdigest(),email,phonenum,s,birthday)
def uploadimage(image,id,des):
    path=os.path.join(imgpath,des,id)
    if not os.path.exists(path):
        os.mkdir(path)
    c=1
    for t in image:
        time=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+'_'+str(c)
        finalpath=os.path.join(path,time,'.',t.content_type)
        t.save(finalpath)
def uploadavatar(image,id):
    uploadimage(image,id,'avatar')
def uploaditemimg(image,itemid):
    uploadimage(image,id,'items')
    return 'insert into users (id,user_name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,r.hexdigest(),email,phonenum,s,birthday)
