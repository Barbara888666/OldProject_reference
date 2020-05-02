import os,datetime
from db import dbop, imgpath,hash
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,hash(password),email,phonenum,s,birthday),False)
