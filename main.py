from flask import Flask,render_template,g
from os import urandom
from db import init

from util.register import register
from util.login import login
from util.search import search
from util.news import news
from util.notice import notice
from util.popular import popular
from util.favorites import favorites
from util.emerge import emerge
from util.detail import detail
from util.seller import seller
from util.personal import personal
from util.mainpage import mainpage
from util.sell import sale
from util.buy import bought

app = Flask(__name__,static_url_path='',template_folder='htmls')
app.secret_key=urandom(16)
#紧急卖卖：卖品，卖品图片，卖家；买的东西，买的描述，买家
#网站通知：最新通知
#分类：分类列表
#高信誉度卖家：卖家名字，卖家卖的最多的分类
#最火的产品：产品名字，产品图片
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(search)
app.register_blueprint(notice)
app.register_blueprint(emerge)
app.register_blueprint(popular)
app.register_blueprint(detail)
app.register_blueprint(news)
app.register_blueprint(favorites)
app.register_blueprint(seller)
app.register_blueprint(personal)
app.register_blueprint(mainpage)
app.register_blueprint(sale)
app.register_blueprint(bought)

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# @app.route('/register')
# def register():
#     return render_template('register.html')
# @app.route('/login')
# def login():
# #     return render_template('login.html')
# @app.route('/emerge')
# def emerge():
#     return render_template('emerge.html')
# @app.route('/favorites')
# def favors():
#     return render_template('favorites.html')
# @app.route('/seller')
# def seller():
#     return render_template('seller_information.html')
# @app.route('/popular')
# def popular():
#     return render_template('popular_products.html')
# @app.route('/news')
# def news():
#     return render_template('my_news.html')
# @app.route('/highpre')
# def highpre():
#     return render_template('high_predibility_seller.html')
# @app.route('/detail')
# def detail():
#     return render_template('商品详情.html')
# @app.route('/notice')
# def notice():
#     return render_template('website_notice.html')
# @app.route('/search',methods=('GET', 'POST'))
# def searchtest():
#     #由后端传送文件的示范
#     file="/images/test.jpg"
#     return render_template('search_web_page.html',file=file)

if __name__=="__main__":
    init()
    app.run(threaded=True,debug=True)
