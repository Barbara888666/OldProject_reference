def getpassword(id):
    return 'select password from users where users.id=%d'%(id)
def idcheck(id):
    return 'select id from users where users.id=%d'%(id)