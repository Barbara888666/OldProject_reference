import json
from json import JSONDecodeError
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