from flask import Flask,render_template
from util.register import register
from util.login import login
from util.search import search
from util.news import news
from util.notice import notice
from util.popular import popular
from util.favorites import favorites
from util.emerge import emerge
from util.detail import detail

#To run this app, set environment variable "FLASK_APP=main.py", FLASK_ENV="development" is optional, allowing debug features
#use python -m flask run to run this app,--host=0.0.0.0 will set the website to public
#dynamic editing is supported, which means you can chagne the code while the website is still running
app = Flask(__name__,static_url_path='',template_folder='htmls')

#static folder means the folder for static html pages
#route() method binds functions to the corresponded URLs
#e.g. /url means the function will preform when user visits yourwebsiteurl/url

# app.register_blueprint(search)


@app.route('/')
def main_page():
    return render_template('main_page.html')
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(search)
app.register_blueprint(notice)
app.register_blueprint(emerge)
app.register_blueprint(popular)
app.register_blueprint(detail)
app.register_blueprint(news)
app.register_blueprint(favorites)
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
    app.environment="development"
    app.run()
