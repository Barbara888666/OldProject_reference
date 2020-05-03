import hashlib
from db import dbop

def pwcheck(id,pw):

    return hashlib.md5().update(pw.encode('utf-8')).hexdigest() == dbop('select password from users where users.id=%d'%(id),True)[0][0]
def idcheck(id):
    return dbop('select id from users where users.id=%d'%(id),True)
def searchitem(itemname):
    return dbop('select item_id,item_name,image_link,item_id,description from items natural join users where items.item_name like %'+itemname,True)
def searchuser(userid):
    return dbop('select * from users where users.id=%d'%(userid),True)