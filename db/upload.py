import os,datetime
from db import dbop, imgpath,hash,uploadimgs,delimgs
import time
"""
此模块包含所有和数据库内容上传修改删除的函数
"""
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date,avatar_name) values (%d,"%s","%s","%s","%s","%s","%s",default_avatar)'%(id,name,hash(password),email,phonenum,s,birthday),False)


def uploadavatar(id:[int,str],avatar):
    """
    上传用户头像
    输入：图片，用户id
    """
    
    p=dbop('select avatar_name from users where users.id='+int(id),True)[0][0]
    if p!='default_avatar.png':
        t=delimgs(p)
        if t!=None:
            print('avatar located in '+p+' does not exist')
    r=uploadimgs(avatar,'avatar',str(id))[0]
    dbop('update users set avatar_name='+r+' where id='+str(id),False)


def uploadalbum(userid:[int,str],images,*seq):
    """
    上传相册内容
    输入：用户id，图片，对应的图片顺序,无返回内容
    """
    r=uploadimgs(images,'album',str(id))
    for t,s in zip(r,range(0,seq):
        dbop('''INSERT INTO albums (owner_id,img_name,seq) values (%d,'%s','%s')'''%(userid,t,s),False)

#删除对应的相册图片，基于文件的顺序
#@param userid:用户id
#@param *seq:对应的顺序
def delalbum(userid:[int,str],*seq):
    r=dbop('select img_name,seq from albums where owner_id='+str(userid),True)
    l=[]
    for t in r:
        if int(t[1]) in seq:
            dbop('delete from albums where seq='+t[1],False)
            l.append(t[0])
    delimgs(*l)

def uploaditem(name,sellerid,description,category='other',price:[float]=None,issell:[bool]=True,image=None):

    """
    上传物品
    输入：物品名，卖家id，描述，类别，价格（可选），是否为出售，图片（可选）,无返回变量
    """
    if not isinstance(sellerid,int):
        sellerid=int(sellerid)
    t=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    p='null'
    if price!=None:
        p=price
    q='''INSERT INTO items (item_name,seller_id,description,added_date,is_urgent,view_time,category,price)VALUES 
    ('%s',%d,'%s','%s','%s',0,'%s',%f);'''%(name,sellerid,description,t,issell,category,p)
    dbop(q,False)
    if image!=None:
        uploadavatar(sellerid,image)
    return dbop('''select item_id from items where item_name="%s" and seller_id="%d" and added_date="%s" and category="%s" and price="%d"
    '''%(name,sellerid,t,category,price),True)[0][0]


def uploadreply(item_id:[int,str],userid:[int,str],content:[str],image=None):
    """
    上传回复
    输入：物品id，用户id，内容，图片（可选），无返回内容
    """
    if isinstance(item_id,str):
        item_id=int(item_id)
    if isinstance(userid,str):
        userid=int(userid)
    q='''INSERT INTO replies (
                        item_id,
                        user_id,
                        reply_content,
                    )
                    VALUES (
                        %d,
                        %d,
                        '%s'
                    );'''%(item_id,userid,content)
    dbop(q,False)

def delreply(replyid:[int,str]):
    r=dbop('select img_name from reply_imgs where reply_id='+str(replyid),True)
    for t in r:
        delimgs(t[0])
    dbop('delete from replies where reply_id='+str(replyid),False)