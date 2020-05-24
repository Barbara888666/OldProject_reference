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
def uploadimg(img,des:str,tid:[int,str],name:str):
    fpath=path.join(imgpath,des,tid)
    if not path.exists(fpath):
        makedirs(fpath)
    suffix=img.filename.split('.')[-1]
    fname='.'.join(name,suffix)
    fp=path.join(fpath,fname)
    if not path.isfile(fp):
        with open(fp):
            pass
    img.save(fp)
def uploadimgs(imgs:list,des:str,tid:[int,str]):
    tid=str(tid)
    r=[]
    for i,n in zip(imgs,range(0,len(imgs))):
        fn=hash(''.join(des,tid),bytes(n))
        uploadimg(i,des,tid,fn)
        r.append('/'.join('imgs',des,tid,fn))
    return r
def delimg(des:str,tid:str):
    dpath=path.join(imgpath,des,tid)
    if path.exists(dpath):
        removedirs(dpath)