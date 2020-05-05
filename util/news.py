from flask import Blueprint,render_template
news=Blueprint('news',__name__)
@news.route('/news')
def new():
    return render_template('my_news.html')
#有多少人想联系我、有多少人收藏我的物品