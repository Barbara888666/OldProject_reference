from flask import Blueprint,render_template,request,session,redirect
from util.utils.filesearch import searchalbum,searchavatar,searchitemimg
from db.search import searchuser,searchitems

seller=Blueprint('seller',__name__)
# @seller.route('/seller/<int:user>')
# def sellers(user):
#     t = searchuser(user)
#     username = t[0][0]
# email = t[0][1]
# phone = t[0][2]
# print(t)
# return render_template('seller_information.html', username=username, email=email, phone=phone)

@seller.route('/testmain/')


def tests():
    if 'id' in session:

        t = searchuser(int(session['id']))
        # a = searchitems()
        # img=searchavatar(int(session['id'])
        # album = searchalbum(int(session['id'])
        #
        # itemimg =searchitemimg()
        username = t[0][0]
        email = t[0][1]
        phone = t[0][2]
        return render_template('maintest.html', username=username, email=email, phone=phone)
    return redirect('/login')




#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类