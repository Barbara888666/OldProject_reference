from flask import Blueprint,render_template
news=Blueprint('news',__name__)
@news.route('/news')
def new():
    return render_template('my_news.html')