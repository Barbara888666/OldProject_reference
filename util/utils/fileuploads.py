import os
from db import imgpath,hash
from os import urandom
from util.utils import uploadimage,delimage

def uploadavatar(image,id):
    rmavatar(id)
    uploadimage([image],id,'avatar',0)
def uploaditemimg(image,itemid:[int,str]):
    uploadimage(image,itemid,'items',*range(0,len(image)))
def uploadalbum(image,id):   
    uploadimage(image,id,'album',*range(0,len(image)))
                    
def rmavatar(id):
    delimage(id,'avatar',0)
def rmalbumimg(id,*seq):
    delimage(id,'album',*seq)
