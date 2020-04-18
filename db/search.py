def getpassword(id):
    return 'select password from users where users.id=%d'%(id)
def idcheck(id):
    return 'select id from users where users.id=%d'%(id)
def searchitem(itemname):
    return 'select item_id,item_name,image_link,item_id,description from items natural join users where items.item_name like %'+itemname
def searchuser(userid):
    return 'select * from users where users.id=%d'%(userid)