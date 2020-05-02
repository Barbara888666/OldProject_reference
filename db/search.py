import hashlib
from db import dbop

<<<<<<< HEAD
def pwcheck(id,pw):   
    return hashlib.md5().update(pw.encode('utf-8')).hexdigest() == dbop('select password from users where users.id=%d'%(id),True)[0][0]
=======
def pwcheck(id,pw):
    t=hashlib.md5()
    t.update(pw.encode(encoding='UTF-8'))
    if t.hexdigest() == dbop('select password from users where users.id=%d'%(id),True)[0][0]:
        return True
    return False
>>>>>>> 263fe55ff6defca4dc35020f634b570383e5c663
def idcheck(id):
    return dbop('select id from users where users.id=%d'%(id),True)
def searchitem(itemname):
    return dbop('select item_id,item_name,image_link,item_id,description from items natural join users where items.item_name like %'+itemname,True)
def searchuser(userid):
    return dbop('select * from users where users.id=%d'%(userid),True)