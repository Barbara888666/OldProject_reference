import os
from util.utils import rjson,getdir,searchimgs

def searchavatar(id):
    return searchimgs(str(id),'avatar')
def searchalbum(id):
    return searchimgs(str(id),'album')
def searchitemimg(itemid):
    return searchimgs(str(itemid),'items')