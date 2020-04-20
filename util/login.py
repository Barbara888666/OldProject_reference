from flask import Blueprint, render_template, jsonify, request

login=Blueprint('login',__name__)

@login.route('/login/',methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('Login.html')
    else:
        password = request.form.get('password'),
        studentnumber = request.form.get('studentnumber'),
        # print(loginput)
        # 根据studentnumber在库里查找：没有 studentnumber 有studentnumber：密码
        resu = {'m': 0}
        # if(loginput['studentnumber']==12345678):result=0
        # elif(loginput['studentnumber']==12345678 and loginput['password']!="liang666"):result=1
        # else:result=100
        if(studentnumber==1):result=0
        elif(studentnumber==12345678 and password!="liang666"):result=1
        else:result=100

        # if studentnumber == 'zhiliao' :
        #     result=0;
        # else:
        #     result=1;
        # if password == 'zhiliao' and password == '111111':
        #     return jsonify({"code": 200, "message": ""})
        # else:
        #     return jsonify({"code": 401, "message": "用户名或密码错误！"})
        print(result)
        if(result==0):
            resu['message']="THIS STUDENTNUMBER IS NOT EXIST"
            # return jsonify(resu)
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


