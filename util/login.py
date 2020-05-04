from flask import Blueprint, render_template, jsonify, request,session,redirect
from db.search import idcheck,pwcheck
login=Blueprint('login',__name__)

@login.route('/login/',methods=['GET','POST'])
def log():

    if request.method == 'GET':
        return render_template('Login.html')
    else:
        logdic = dict(
            username=request.form.get('username'),
            password=request.form.get('password')
        )
        render_template('Register.html', **logdic)
        studentnumber=logdic['username']
        password=logdic['password']
        resu = {'m': 0}
        if idcheck(int(studentnumber)) is None:
            resu['message']="THIS STUDENTNUMBER IS NOT EXIST"
            return jsonify({"code":1,"message":"学号格式错误"})
        elif not pwcheck(int(studentnumber),password):
            resu['message'] = "WRONG PASSWORD OR WRONG STUDNETNUMBER"
            return jsonify({"code":2,"message":"密码错误"})
        else:
            session['id']=studentnumber
            resu['message'] = "LOGIN SUCCESSFULLY"
            print(resu['message'])
            return jsonify({"code": 3, "message": "好了"})
        return jsonify(resu)
@login.route('/logout')
def out():
    if 'id' in session:
        session.pop('id',None)
        return redirect('/')
    return redirect('/login')