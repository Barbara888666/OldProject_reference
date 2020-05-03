import hashlib
from db import dbop

def pwcheck(id,pw):
    t=hashlib.md5()
    t.update(pw.encode(encoding='UTF-8'))
    if t.hexdigest() == dbop('select password from users where users.id=%d'%(id),True)[0][0]:
        return True
    return False
def idcheck(id):
    return dbop('select id from users where users.id=%d'%(id),True)
def searchitems(itemname,page,*category):
    query='''select item_id,item_name,user_name from items natural join users where items.seller_id=users.id and items.category='''+"'"+category[0]+"'"+''' and items.item_name like '''+"'%"+itemname+"%'"+'limit 10 offset '+str(page)
    return dbop(query,True)
def searchitem(item_id):
    return dbop('select * from items where items.item_id='+item_id,True)
def searchitemnum(itemname,*category):
    query='select count(*) from items where category='+"'"+category[0]+"'"+' and items.item_name like '+"'%"+itemname+"%'"
    return dbop(query,True)[0][0]
def searchuser(userid):
    return dbop('select id,user_name,email,phone_number,sex from users where users.id=%d'%(userid),True)