import hashlib
def registeraccount(id,name,password,email):
    r=hashlib.md5()
    r.update(password.encode(encoding='UTF-8'))
    return 'insert into users (id,name,password,email) values (%d,%s,%s,%s)'%(id,name,r.hexdigest(),email)
