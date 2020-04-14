from flask import Blueprint,render_template
search=Blueprint('search',__name__)
# @search.route('/search',classmethod=('GET','POST'))
# def searchtest():
#     #由后端传送文件的示范
#     file="/images/test.jpg"
#     return render_template('search_web_page.html',file=file)
@search.route('/search')
def searchtest():
    return render_template('search_web_page.html')
