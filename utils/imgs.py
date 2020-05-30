from config import imgpath
from os import path,makedirs,removedirs
from hashlib import md5
def hash(word:str='',salt:bytes=None):
    if word=='':
        return ''
    if not bytes==None:
        h=md5(salt)
    else:
        h=md5()
    h.update(word.encode('UTF-8'))
    return h.hexdigest()
def uploadimg(img,des:str,tid:str,name:str):
    fpath=path.join(imgpath,des,tid)
    if not path.exists(fpath):
        makedirs(fpath)
    suffix=img.filename.split('.')[1]
    print(suffix)
    fname='.'.join([name,suffix])
    print(fname)
    fp=path.join(fpath,fname)
    if not path.isfile(fp):
        with open(fp,'w'):
            pass
    img.save(fp)
    return fname
def uploadimgs(imgs:list,des:str,tid:[int,str]):
    tid=str(tid)
    r=[]
    for i,n in zip(imgs,range(0,len(imgs))):
        fn=hash(des+tid,bytes(n))
        r.append('/'.join(['imgs',des,tid,uploadimg(i,des,tid,fn)]))
    return r
def delimg(des:str,tid:str):
    dpath=path.join(imgpath,des,tid)
    if path.exists(dpath):
        removedirs(dpath)