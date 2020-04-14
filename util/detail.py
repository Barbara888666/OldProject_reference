from flask import Blueprint,render_template
detail=Blueprint('detail',__name__)
@detail.route('/detail')
def details():
    return render_template('商品详情.html')