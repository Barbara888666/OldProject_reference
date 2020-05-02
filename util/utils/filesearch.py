import os
from db import imgpath
def searchimgs(path):
    return os.listdir(path)
def searchavatar(id):
    if isinstance(id,int):
        id=str(id)
    path=os.path.join(imgpath,'avatar',id)
    if not os.path.exists(path):
        return None
    return searchimgs(path)