from flask import Blueprint,render_template
emerge=Blueprint('emerge',__name__)
@emerge.route('/emerge')
def emerges():
    return render_template('emerge.html')
#买列表：想买的物品，描述，买家名字
#卖列表：商品图片，商品名字，分类，卖家名字