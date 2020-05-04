from flask import Blueprint,render_template,request,session,redirect
from db.search import searchuser
seller=Blueprint('seller',__name__)
@seller.route('/seller/<int:userid>/')
def sellers(userid):
    t = searchuser(userid)
    username = t[0][1]
    email = t[0][2]
    phone = t[0][3]
    return render_template('seller_information.html', username=username, email=email, phone=phone)


#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类