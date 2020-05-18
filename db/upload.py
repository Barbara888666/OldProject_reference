import os,datetime
from db import dbop, imgpath,hash,uploadimgs,delimgs,delimgf,getctime,getsalt
"""
此模块包含所有和数据库内容上传修改删除的函数
"""
def registeraccount(id,name,password,email,phonenum,sex,birthday):
    salt=getsalt()
    s='null'
    if sex=='male':
        s='true'
    else:
        s='false'
    dbop('insert into users (id,user_name,password,email,phone_number,sex,birth_date,avatar_name,salt) values (%d,"%s","%s","%s","%s","%s","%s","default_avatar.png","%s")'%(id,name,hash(password,salt),email,phonenum,s,birthday,salt),False)

def changeinfo(userid:[int,str],name:str=None,email:str=None,phonenum:str=None,sex:str=None,birthday:str=None):
    """
    改变个人信息
    参量: id:用户id
    可选参量:用户名，邮箱，手机号码，性别，生日
    """
    q=['update users set']
    if name!=None:
        q.append("name='"+name+"'")
    if email!=None:
        q.append("email='"+email+"'")
    if phonenum!=None:
        q.append("phone_number='"+phonenum+"'")
    if sex!=None:
        if sex=='male':
            q.append('sex=true')
        if sex=='female':
            q.append('sex=false')
    if birthday!=None:
        q.append("birthday='"+birthday+"'")
    q.append('where id='+str(userid)+';')
    dbop(' '.join(q),False)
def uploadavatar(id:[int,str],avatar):
    """
    上传用户头像
    输入：图片，用户id
    """
    delimgf('avatar',str(id))
    r=uploadimgs(avatar,'avatar',str(id))[0]
    dbop('update users set avatar_name='+r+' where id='+str(id),False)

def addviewtime(itemid:[int,str]):
    dbop('update items set view_time=view_time+1 where item_id='+itemid,False)


def uploadalbum(userid:[int,str],images,*seq):
    """
    上传相册内容
    输入：用户id，图片，对应的图片顺序,无返回内容
    """
    r=uploadimgs(images,'album',str(id))
    for t,s in zip(r,range(0,seq)):
        dbop('''INSERT INTO albums (owner_id,img_name,seq) values (%d,'%s','%s')'''%(userid,t,s),False)


def uploaditemimg(itemid:str,imgs):
    r=[None]
    if imgs!=None:
        imgs=[imgs]
        r=uploadimgs(imgs,'items',itemid)
    for t,n in zip(r,range(0,len(imgs))):
        q='''
        INSERT INTO item_imgs (
                          item_id,
                          img_name,
                          seq
                      )
                      VALUES (
                          %s,
                          '%s',
                          %d
                      );
        '''%(itemid,t,n)
        dbop(q,False)

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

def uploaditem(name:str,sellerid:[int,str],description:str,category='other',price:[float]=None,issell:bool=True,situation:str='Brand new',image=None):

    """
    上传物品
    输入：物品名，卖家id，描述，类别，价格（可选），是否为出售，图片（可选）,无返回变量
    """
    if not isinstance(sellerid,int):
        sellerid=int(sellerid)
    t=getctime()
    p='null'
    if price!=None:
        p=price
    s=0
    if situation=='Brand new':
        pass
    elif situation=='Slightly used':
        s=1
    elif situation=='Used':
        s=2
    elif situation=='Left over':
        s=3
    q='''INSERT INTO items (item_name,seller_id,description,added_date,is_sell,view_time,category,price,situation)VALUES 
    ('%s',%d,'%s','%s','%s',0,'%s',%f,%d);'''%(name,sellerid,description,t,issell,category,p,s)
    r=dbop(q,False,'items')
    uploaditemimg(str(r),image)

#删除物品
#@param itemid:物品id
def delitem(itemid:[int,str]):
    itemid=str(itemid)
    q='delete from items where item_id='+itemid
    dbop(q,False)
    delimgf('items',itemid)    

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
                        added_date
                    )
                    VALUES (
                        %d,
                        %d,
                        '%s',
                        '%s'
                    );'''%(item_id,userid,content,getctime())
    r=dbop(q,False,'replies')
    if image!=None:
        
        a=uploadimgs(image,'replies',r)
        for t,n in zip(a,range(0,len(a))):
            dbop('''
            INSERT INTO reply_imgs (
                           reply_id,
                           img_name,
                           seq
                       )
                       VALUES (
                           %s,
                           '%s',
                           %d
                       );
            '''%(r,t,n),False)

#删除回复
#@param replyid:回复内容的id
def delreply(replyid:[int,str]):
    delimgf('replies',replyid)
    dbop('delete from replies where reply_id='+str(replyid),False)

#关注某用户
#@param srcid:此用户的id
#@param targetid: 要关注的用户的id
def like(srcid:[int,str],targetid:[int,str]):
    strid=str(srcid)
    targetid=str(targetid)
    dbop('''INSERT INTO likes (self_id,target_id) VALUES (%s,%s );'''%(strid,targetid),False)

#取关某用户，参照关注某用户的使用方法
def unlike(srcid:[int,str],targetid:[int,str]):
    strid=str(srcid)
    targetid=str(targetid)
    dbop('delete from likes where self_id='+strid+' and target_id='+targetid)

def sendchat(srcid:[int,str],desid:[int,str],content:str,images='null'):
    """
    发送聊天内容
    参量：发送者id，接收者id，内容，图片（可选，限制一张）
    """
    srcid=str(srcid)
    desid=str(desid)
    r=uploadimgs(images,'chats','chat')
    dbop('''
    INSERT INTO chats (
                      sender_id,
                      receiver_id,
                      content,
                      send_time
                      image_name
                  )
                  VALUES (
                      %s,
                      %s,
                      '%s',
                      '%s'
                      '%s'
                  );
    '''%(srcid,desid,content,getctime(),r),False)

def sendreport(targetid:str,typen,typeid:str,reason):
    q='''insert into %s (%s,report_reason) values (%s,%s)'''%(typen,typeid,targetid,reason)
    dbop(q,False)

#上传用户举报内容
#@param targetid: 被举报用户的id
#@param reason: 理由
def senduserreport(targetid:[int,str],reason:str):
    sendreport(targetid,'user_reports','target_id',reason)

#举报物品，参照举报用户
def senditemreport(targetid:[int,str],reason:str):
    sendreport(targetid,'item_reports','item_id',reason)
def sendreplyreport(targetid:[int,str],reason:str): 
    sendreport(targetid,'reply_reports','target_reply',reason)

def likecategory(srcid:[int,str],category='other'):
    strid = str(srcid)
    q='''insert into likes_category (self_id,category) values (%s,%s )'''%(strid,category)
    dbop(q,False)

def unlikecategory(srcid:[int,str],category='other'):
    strid = str(srcid)
    dbop('delete from likes_category where self_id=' + strid + ' and category=' + category)

def addlikenotice(userid:[int,str],seen:bool=False,likerid:[int,str]):
    strid = str(userid)
    strlikerid = str(likerid)
    dbop('insert into like_notifications (user_id,seen,liker_id) values (' + strid + ','+ seen +','+strlikerid+')')
def adddeletenotice(userid:[int,str],seen:bool=False,itemid:[int,str],replyid:[int,str]):
    strid = str(userid)
    stritemid = str(itemid)
    strreplyid = str(replyid)
    dbop('insert into delete_notifications (user_id,seen,item_id,reply_id) values (' + strid + ','+ seen +',' + stritemid +','+strreplyid  + ')')
def addreplynotice(userid:[int,str],seen:bool=False,replyid:[int,str],replierid:[int,str]):
    strid = str(userid)
    strreplyid = str(replyid)
    strreplierid = str(replierid)
    dbop('insert into reply_notifications (user_id,seen,reply_id,replier_id) values (' + strid + ','+ seen + ',' + strreplyid  +',' + strreplierid  +')')

def deletedeletenotice(userid:[int,str],notiid:[int,str]):
    strid = str(userid)
    notistrid =str(notiid)
    dbop('delete from delete_notifications where user_id=' + strid + ' and noti_id=' + notistrid)

def deletelikenotice(userid:[int,str],notiid:[int,str]):
    strid = str(userid)
    notistrid =str(notiid)
    dbop('delete from like_notifications where user_id=' + strid + ' and noti_id=' + notistrid)

def deletereplyotice(userid:[int,str],notiid:[int,str]):
    strid = str(userid)
    notistrid =str(notiid)
    dbop('delete from reply_notifications where user_id=' + strid + ' and noti_id=' + notistrid)


