#encoding: utf-8
from utils.imgs import uploadimgs,delimg
def uploadproductimgs(imglist:list,itemid:[int,str]):
    return uploadimgs(imglist,'products',itemid)

def delproductimgs(itemid:[int,str]):
    delimg('products',str(itemid))

def uploadavatar(avatar,userid:[int,str]):
    return uploadimgs([avatar],'avatar',userid)[0]

def delavatar(userid:[int,str]):
    delimg('avatar',str(userid))