import json
from json import JSONDecodeError
from os import path,listdir,urandom,makedirs,remove
from db import imgpath,hash
def uploadimage(image:list,id,des,*seq):
    tid=id
    
    if not isinstance(id,str):
        tid=str(id)
    
    rpath=path.join(imgpath,des,tid)
    spath=path.join(rpath,"seq.json")
    
    if not path.exists(rpath):
        makedirs(rpath)
    
    seqlist={}
    
    if path.exists(spath):
        seqlist.update(rjson(spath))
   
    for t,n in zip(image,seq):
        tname=hash(str(urandom(8)))+'.'+t.filename.split('.')[-1]
        finalpath=path.join(rpath,tname)
        if not path.exists(finalpath):
            a=open(finalpath,'w')
            a.close()
        t.save(finalpath)
        seqlist.update({n:finalpath})
    wjson(spath,seqlist)

def delimage(id,des,*seq):
    rpath=path.join(imgpath,des,str(id))
    
    if path.exists(rpath):
        finalpath=path.join(rpath,"seq.json")
        
        if path.exists(finalpath):
            t=rjson(finalpath)
            
            for tseq in seq:
                tf='None'

                if str(tseq) in t:
                    tf=t.pop(str(tseq))
                
                if path.exists(tf):
                    remove(tf)
            wjson(finalpath,t)

def jsonio(dir,mode,dict):
    with open(dir,mode=mode) as d:
        if mode=='r':
            try:
                t=json.loads(d.read())
                return t
            except JSONDecodeError: 
                return None
        elif mode=='w':
            d.write(json.dumps(dict))
def rjson(dir):
    return jsonio(dir,'r',None)
def wjson(dir,dict):
    jsonio(dir,'w',dict)

def getdir(*dirseq):
    r=imgpath
    for t in dirseq:
        r=path.join(r,t)
    if path.exists(r):
        return r
    return None
def searchimgs(id:str,des):
    p=getdir(des,str(id),'seq.json')
    if p is not None:
        t=rjson(p)
        if t is not None:
            return t["0"]
    return None