import hashlib
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    r=hashlib.md5()
    r.update(password.encode(encoding='UTF-8'))
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    return 'insert into users (id,name,password,email,phone_number,sex,birth_date) values (%d,"%s","%s","%s","%s","%s","%s")'%(id,name,r.hexdigest(),email,phonenum,s,birthday)
