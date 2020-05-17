from db import imgpath
from os import path
def getavatarpath(userid:[int,str],imgname:str):
    userid=str(userid)
    return path.join(imgpath,'avatar',userid,imgname)
def getitemimgpath(itemid:[int,str],imgname:str):
    itemid=str(itemid)
    return path.join(imgpath,'items',itemid,imgname)