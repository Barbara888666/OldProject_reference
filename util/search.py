def getpassword(id):
    return 'select password from users where users.id=%d'%(id)