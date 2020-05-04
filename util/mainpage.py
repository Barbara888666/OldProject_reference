from flask import Blueprint,render_template,session
mainpage=Blueprint('main_page',__name__)
@mainpage.route('/')
def main_page():
    userid=None
    if 'id' in session:
        userid=session['id']
    return render_template('main_page.html',userid=userid)