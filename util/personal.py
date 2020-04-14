from flask import Blueprint,render_template
personal=Blueprint('personal',__name__)
@personal.route('/personal')
def personals():
    return render_template('personal_information.html')
#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类