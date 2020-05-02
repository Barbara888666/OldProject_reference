import os,datetime,json
from db import imgpath,hash
from os import urandom
from util.utils import rjson,wjson
def uploadimage(image:list,id,des,*seq):
    tid=id
    if isinstance(id,int):
        tid=str(id)
    path=os.path.join(imgpath,des,tid)
    spath=os.path.join(path,"seq.json")
    if not os.path.exists(path):
        os.makedirs(path)
    seqlist={}
    if os.path.exists(spath):
        seqlist.update(rjson(spath))
    for t,n in zip(image,seq):
        tname=hash(str(urandom(8)))+'.'+t.filename.split('.')[-1]
        finalpath=os.path.join(path,tname)
        if not os.path.exists(finalpath):
            a=open(finalpath,'w')
            a.close()
        t.save(finalpath)
        seqlist.update({n:finalpath})
    wjson(spath,seqlist)
def uploadavatar(image,id):
    rmavatar(id)
    uploadimage([image],id,'avatar',0)
def uploaditemimg(image,itemid):
    uploadimage(image,id,'items',*range(0,len(image)))
def uploadalbum(image,id):   
    uploadimage(image,id,'album',*range(0,len(image)))
def delimage(id,des,*seq):
    path=os.path.join(imgpath,des,str(id))
    print("path:"+path)
    if os.path.exists(path):
        finalpath=os.path.join(path,"seq.json")
        if os.path.exists(finalpath):
            t=rjson(finalpath)
            print(t)
            for tseq in seq:
                tf=t.pop(str(tseq))
                if os.path.exists(tf):
                    os.remove(tf)
            wjson(finalpath,t)
                    
def rmavatar(id):
    delimage(id,'avatar',0)
