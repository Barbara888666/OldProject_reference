from flask import Blueprint,render_template,request,session,redirect
from db.search import searchuser
personal=Blueprint('personal',__name__)
@personal.route('/personal')
def personals():
    if 'id' in session:
        t=searchuser(int(session['id']))
        username=t[0][1]
        email=t[0][2]
        phone = t[0][3]
        return render_template('personal_information.html',username=username,email=email,phone=phone)
    # return redirect('/login')

#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类