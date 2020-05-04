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
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    q='''INSERT INTO items (item_name,seller_id,description,added_date,is_urgent,view_time,category,price)VALUES 
    ('%s',%d,'%s','%s','%s',0,'%s',%d);'''%(name,sellerid,description,t,isurgent,category,price)
    dbop(q,False)
    return dbop('''select item_id from items where item_name="%s" and seller_id="%d" and added_date="%s" and category="%s" and price="%d"
    '''%(name,sellerid,t,category,price),True)[0][0]