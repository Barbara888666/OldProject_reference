import re

from flask import Blueprint, render_template, request, jsonify

register=Blueprint('register',__name__)

@register.route('/register/',methods=['GET','POST'])
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

