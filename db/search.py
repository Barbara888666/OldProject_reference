import hashlib
from db import dbop,hash

def pwcheck(id,pw):
    r=dbop('select password,salt from users where users.id=%d'%(id),True)[0]
    t=hash(pw,r[1])
    return t == r[0]
def idcheck(id):
    return dbop('select id from users where users.id=%d'%(id),True)
# 输入：可选项：物品名, 类别，页面，排序选项（格式：“{列名称：asc/desc}”,列名称请见名为items的table）
# 返回带有物品id，物品名称，用户id，物品首个图片的表中表
def searchitems(itemname:str=None,page:int=None,orderby:dict=None,category='other'):
    query='''select item_id,item_name,user_name,img_name from items natural join users natural join item_imgs where items.seller_id=users.id  and item_imgs.item_id=items.item_id and item_imgs.seq=0'''
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
def searchreply_imgs(reply_id):
    return dbop('select * from reply_imgs where reply_imgs.reply_id='+reply_id,True)
#输入回复id,返回该回复中的图片以及图片所对于的顺序
def searchchat(chat_id):
    return dbop('select * from chat where chat.chat_id='+chat_id,True)
#输入聊天id，返回该聊天的寄件人和收件人id，以及内容和发送时间