#encoding: utf-8
from utils.imgs import uploadimgs
def uploadproductimgs(imglist:list,itemid:[int,str]):
    return uploadimgs(imglist,'products',itemid)
