from flask import Flask,render_template,request,redirect,url_for,jsonify

app = Flask(__name__)

# AJAX(ajax)
# Async JavaScript And XML
# Async（异步）：网络请求是异步的。
# JavaScript：JavaScript语言
# And：并且
# XML：JSON

@app.route('/')
def index():
    return '这是首页！'

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('log.html')
    else:
        # 和前端约定好，发送网络请求，不管用户名和密码是否验证成功
        # 我都返回同样格式的json对象给你
        # {"code":200,"message":""}
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'zhiliao' and password == '111111':
            return jsonify({"code":200,"message":""})
        else:
            return jsonify({"code":401,"message":"用户名或密码错误！"})

if __name__ == '__main__':
    app.run(debug=True)
