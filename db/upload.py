import os,datetime
from db import dbop, imgpath,hash,uploadimgs
import time
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date,avatar_name) values (%d,"%s","%s","%s","%s","%s","%s",default_avatar)'%(id,name,hash(password),email,phonenum,s,birthday),False)
#上传用户头像
#输入：图片，用户id
def uploadavatar(id:int,avatar):
     r=uploadimgs(avatar)[0]
     dbop('update users set avatar_name='+r,False)
     
def uploaditem(name,sellerid,description,category,price,issell='true'):
    if not isinstance(sellerid,int):
        sellerid=int(sellerid)
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    q='''INSERT INTO items (item_name,seller_id,description,added_date,is_urgent,view_time,category,price)VALUES 
    ('%s',%d,'%s','%s','%s',0,'%s',%d);'''%(name,sellerid,description,t,issell,category,price)
    dbop(q,False)
    return dbop('''select item_id from items where item_name="%s" and seller_id="%d" and added_date="%s" and category="%s" and price="%d"
    '''%(name,sellerid,t,category,price),True)[0][0]