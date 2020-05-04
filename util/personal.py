from flask import Blueprint,render_template,request
from db.search import searchuser
personal=Blueprint('personal',__name__)
@personal.route('/personal/<userid>/')
def personals(userid):
    username=searchuser(userid=userid)[0][1]
    email=searchuser(userid=userid)[0][2]
    phone = searchuser(userid=userid)[0][3]


    return render_template('personal_information.html',username=username,email=email,phone=phone)
#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类