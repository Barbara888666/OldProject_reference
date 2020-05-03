import os,datetime
from db import dbop, imgpath,hash
import time
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,hash(password),email,phonenum,s,birthday),False)
def uploaditem(name,sellerid,description,category,price,isurgent='false'):
    if not isinstance(sellerid,int):
        sellerid=int(sellerid)
    q='''INSERT INTO items (item_name,seller_id,description,added_date,is_urgent,view_time,category,price)VALUES 
    ('%s',%d,'%s','%s','%s',0,'%s',%d);'''%(name,sellerid,description,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),category,isurgent,price)
    dbop(q,False)