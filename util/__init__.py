
from os import path
def getavatarpath(userid:[int,str],imgname:str):
    userid=str(userid)
    return path.join('images','avatar',userid,imgname)
def getitemimgpath(itemid:[int,str],imgname:str):
    itemid=str(itemid)
    return '/images/items/'+itemid+'/'+imgname