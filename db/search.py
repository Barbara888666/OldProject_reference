def getpassword(id):
    return 'select password from users where users.id=%d'%(id)
def idcheck(id):
    return 'select id from users where users.id=%d'%(id)
def searchitem(itemname):
    return 'select * from items where items.name like %'+itemname
def searchuser(userid):
    return 'select * from users where users.id=%d'%(userid)