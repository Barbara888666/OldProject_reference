import hashlib
from db import dbop,hash,getctime

def pwcheck(id,pw):
    r=dbop('select password,salt from users where users.id=%d'%(id),True)[0]
    t=hash(pw,r[1])
    return t == r[0]
def idcheck(id):
    return dbop('select id from users where users.id=%d'%(id),True)
# 输入：可选项：物品名, 类别，页面，排序选项（格式：“{列名称：asc/desc}”,列名称请见名为items的table）
# 返回带有物品id，物品名称，用户id，物品首个图片的表中表
def searchitems(itemname:str=None,page:int=None,orderby:dict=None,category='other'):
    query='''select items.item_id,item_name,user_name,img_name from items cross join users cross join item_imgs where items.seller_id=users.id  and item_imgs.item_id=items.item_id and item_imgs.seq=0 '''
    if itemname!=None:
        query=query+'and items.item_name like '''+"'%"+itemname+"%' "
    query=query+'''and items.category='''+"'"+category+"' "
    if orderby!=None:
        for k in orderby:
            query=query+"order by "+k+" "+orderby[k]+" "
    if page!=None:
        query=query+'limit 10 offset '+str(page)
    return dbop(query,True)
#输入物品id，返回物品的所有信息
def searchitem(item_id):
    return dbop('select * from items where items.item_id='+item_id,True)[0]

#输入物品id，返回物品的图片以及图片对应的顺序
def searchitemimgs(item_id:[str,int]):
    return dbop('select img_name,seq from item_imgs where item_id='+str(item_id)+';')
#输入物品id和类别，返回当前结果的个数
def searchitemnum(itemname,*category):
    query='select count(*) from items where category='+"'"+category[0]+"'"+' and items.item_name like '+"'%"+itemname+"%'"
    return dbop(query,True)[0][0]
#输入用户id，返回名字邮件电话性别出生日期和头像名称
def searchuser(userid):
    return dbop('select user_name,email,phone_number,sex,birth_date,avatar_name from users where users.id=%d'%(userid),True)

def searchalbums(owner_id):
    return dbop('select img_name,seq from albums where albums.owner_id='+owner_id,True)
#输入用户id，返回该用户相簿中的图片以及图片所对应的顺序
def whohelikes(user_id):
    return dbop('select user_name，id from likes natural join users where likes.target_id=users.id and likes.self_id='+user_id,True)
#输入用户id，返回所有被该用户关注的用户的名字及id
def wholikeshim(user_id):
    return dbop('select user_name,id from likes natural join users where likes.self_id=users.id and likes.target_id='+user_id,True)
#输入用户id，返回所有关注该用户的用户的名字及id
def searchreplies(item_id):
    return dbop('select user_name,user_id,reply_content,added_date from replies natural join users where users.id=replies.user_id and replies.item_id='+item_id,True)
#输入回复id，返回该用户名字与id，所回复项目的名字与id,以及添加该回复的日期
def searchreply_imgs(item_id):
    return dbop('select user_name,user_id,item_name,seq from reply_imgs natural join items natural join users where item_id=reply_imgs.item_id and users.id=items.item_id and items.item_id='+item_id,True)
#输入回复id,返回该回复中的图片以及图片所对于的顺序


def searchreport(userid,itype,typeid):
    return dbop('select * from '+itype+' where '+typeid+'='+userid)

#返回所有关于用户举报的内容
def searchuserreport(userid):
    return searchreport(userid,'user_reports','target_id')

#返回所有关于物品的举报内容
def searchitemreport(itemid):
    return searchreport(itemid,'item_reports','item_id')

#返回所有关于回复的举报内容
def searchreplyreport(rid):
    return searchreport(rid,'reply_reports','target_reply')

def searchbanneduser():
    return dbop('select * from banned_user',True)

#输入用户id检验是否被ban
def checkifbanned(userid:[int,str]):
    userid=str(userid)
    return dbop('select * from banned_user where user_id='+userid+' and unban_date>'+getctime().split(' ')[0],True)!=[]
def searchchat(user_id_1,user_id_2):
    return dbop('select content and send_time from chat where chat.sender.id='+user_id_1+' and chat.receiver.id='+user_id_2,True)
#输入聊天id，返回该聊天的寄件人和收件人id，以及内容和发送时间

def whatcategoryhelikes(userid):
    return dbop('select category from likes_category where likes_category.self_id='+userid,True)
#输入用户id，返回该用户所关注的物品种类

def wholikesthiscategory(category):
    return dbop('select self_id from likes_category where likes_category.category='+category,True)
#输入物品种类，返回关注该物品的用户
