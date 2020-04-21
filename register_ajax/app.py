from flask import Flask,render_template,request,redirect,url_for,jsonify
import re
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

@app.route('/register/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('Register.html')
    else:
        dic = dict(
            username=request.form.get('username'),
            password=request.form.get('password'),
            studentnumber=request.form.get('studentnumber'),
            name=request.form.get('name'),
            tel=request.form.get('tel'),
            gender=request.form.get('gender'),
            email=request.form.get('email')
        )
        render_template('Register.html',**dic)
        print(dic)
        # 和前端约定好，发送网络请求，不管用户名和密码是否验证成功
        # 我都返回同样格式的json对象给你
        # {"code":200,"message":""}
        resul = {'username': 0}
        for k in dic.keys():
            if k=='username':
                if re.search('^[\u4E00-\u9FA5A-Za-z0-9]+$', dic['username']):
                    resul['username'] ="USERNAME CORRECT"
                else:
                    resul['username']="'PLEASE INPUT THE TRUE USERNAME:中文、英文、数字但不包括下划线等符号'"
            elif k=='password':
                if re.search('^[a-zA-Z]\w{5,17}$', dic['password']):
                    resul['password'] ="PASSWORD CORRECT"
                else:
                    resul['password'] ="PLEASE INPUT THE TRUE PASSWORD:以字母开头，长度在6~18之间，只能包含字母、数字和下划线"
            if k=='studentnumber':
                if re.search('^\d{8}$', dic['studentnumber']):
                    resul['studentnumber'] ="STUDENTNUMBER CORRECT"
                else:
                    resul['studentnumber']="PLEASE INPUT THE TRUE STUDENTNUMBER:八位数字"
            elif k=='name':
                if re.search('^.{2,10}$$', dic['name']):
                    resul['name'] ="NAME CORRECT"
                else:
                    resul['name'] ="PLEASE INPUT THE TRUE NAME:长度为1-10的所有字符"
            elif k=='tel':
                if re.search('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$', dic['tel']):
                    resul['tel'] ="TELEPHONE CORRECT"
                else:
                    resul['tel'] ="PLEASE INPUT THE TRUE TELEPHONE"
            elif k=='gender':
                if dic['gender']=='male':
                    resul['gender'] ="GENDER CORRECT"
                elif dic['gender']=='female':
                    resul['gender'] ="GENDER CORRECT "
                else:
                    resul['gender'] = "tian"
            elif k=='email':
                if re.search('^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$', dic['email']):
                    resul['email'] ="EMAIL CORRECT"
                else:
                    resul['email'] ="PLEASE INPUT THE TRUE EMAIL"
        if(re.search('CORRECT$',resul['studentnumber'])
                                and re.search('CORRECT$',resul['username'])
                                and re.search('CORRECT$',resul['email'])
                                and re.search('CORRECT$', resul['gender'])
                                and re.search('CORRECT$', resul['tel'])
                                and re.search('CORRECT$', resul['password'])
                                and re.search('CORRECT$', resul['name'])
        ): resul['result'] ="sucess"

        return jsonify(resul)


        # if re.search('^\d{8}$', dic['password']):
        #     return jsonify({"code":200,"message":"学号格式正确","m":"正确"})
        # else:
        #     return jsonify({"code":201,"message":"学号格式错误","m":"错误"})

#现在又好几个需要验证 每一条都要判断是否vaild
# 显示的方式是每一个的后面都输出正确或者错
# 只有提交post再显示所有成功与否
# post后就要一次判断所有的对错 一共36种可能性 return后html只接收一次信息
# 或者是按条目定义函数 每个都自己更新 没有return传不到html页面里
# 所以试着判断两个 一个函数两个传参

@app.route('/login/',methods=['GET','POST'])
def log():
    if request.method == 'GET':
        return render_template('log.html')
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



if __name__ == '__main__':
    app.run(debug=True)
