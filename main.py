from flask import Flask,render_template
#To run this app, set environment variable "FLASK_APP=main.py", FLASK_ENV="development" is optional, allowing debug features
#use python -m flask run to run this app,--host=0.0.0.0 will set the website to public
#dynamic editing is supported, which means you can chagne the code while the website is still running
app = Flask(__name__,static_url_path='',template_folder='htmls')
#static folder means the folder for static html pages
#route() method binds functions to the corresponded URLs
#e.g. /url means the function will preform when user visits yourwebsiteurl/url
@app.route('/')
def main_page():
    return render_template('main_page.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/favorites')
def favors():
    return render_template('favorites.html')
@app.route('/search',methods=('GET', 'POST'))
def searchtest():
    file="/images/test.jpg"
    return render_template('search_web_page.html',file=file)