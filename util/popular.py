from flask import Blueprint,render_template
popular=Blueprint('popular',__name__)
@popular.route('/popular')
def populars():
    return render_template('popular_products.html')
#商品名字，商品图片，卖家