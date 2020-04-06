from flask import Flask,render_template
#To run this app, set environment variable "FLASK_APP=main.py", FLASK_ENV="development" is optional, allowing debug features
#use python -m flask run to run this app,--host=0.0.0.0 will set the website to public
#dynamic editing is supported, which means you can chagne the code while the website is still running
app = Flask(__name__,static_url_path='',static_folder='htmls')
#static folder means the folder for static html pages
#route() method binds functions to the corresponded URLs
#e.g. /url means the function will preform when user visits yourwebsiteurl/url
@app.route('/')
def main_page():
    return app.send_static_file('main_page.html')
@app.route('/register')
def register():
    return app.send_static_file('register.html')
@app.route('/login')
def login():
    return app.send_static_file('login.html')
@app.route('/favorites')
def favors():
    return app.send_static_file('favorites.html')
@app.route('/search')
def searchtest():
    #图片和css无法显示
    return app.send_static_file('search_web_page.html')