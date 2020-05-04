from flask import Blueprint, render_template, jsonify, request

login=Blueprint('login',__name__)

@login.route('/login/',methods=['GET','POST'])
def log():

    if request.method == 'GET':
        return render_template('Login.html')
    else:
        password = request.form.get('password'),
        studentnumber = request.form.get('studentnumber'),

        if(result==0):
            resu['message']="THIS STUDENTNUMBER IS NOT EXIST"
            return jsonify({"code":1,"message":"学号格式错误"})
        elif(result==1):
            resu['message'] = "WRONG PASSWORD OR WRONG STUDNETNUMBER"
            return jsonify({"code":2,"message":"密码错误"})
        else:
            resu['message'] = "LOGIN SUCCESSFULLY"
            print(resu['message'])
            return jsonify({"code": 3, "message": "好了"})
        # print(resu)
        # if studentnumber == 'm':
        #     return jsonify({"code": 1, "message": "学号格式错误"})
        # elif studentnumber == 'zhiliao' and password == '111111':
        #     return jsonify({"code":2,"message":"用户名或密码错误！"})
        # else:
        #     return jsonify({"code":3,"message":"成了！"})
        # json_str = json.dumps(resu)
        # return json_str, 200, {"Content-Type": "application/json"}
        return jsonify(resu)


