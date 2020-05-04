import os
from flask import Flask, render_template, request, flash, Blueprint,session,redirect

sell=Blueprint('sell',__name__)
@sell.route('/sell/', methods=['GET', 'POST'])
def sell_item():
        if request.method == 'GET':
            if 'id' not in session:
                return redirect('/login')
            return render_template('sell.html')
        else:
            dic = dict(
                Category=request.form.get('Category'),
                Situation=request.form.get('Situation'),
                time=request.form.get('time'),
                Short_term=request.form.get('short time'),
                long_time=request.form.get("long time"),
                Note=request.form.get('Note'),
            )
            print(dic)
            f = request.files['pic']
            render_template('sell.html', **dic)
            resul={'start':0}

            if(f==None):
                resul['picture'] = "wrong"
            else:
                basepath = os.path.dirname(__file__)  # 当前文件所在路径
                print(basepath)
                from werkzeug.utils import secure_filename
                upload_path = os.path.join(basepath, 'upload_file_dir', secure_filename(f.filename))
                # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                print(upload_path)
                upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径
                print(upload_path)
                f.save(upload_path)
                resul['picture'] = "CORRECT"


            # path = Register_Login + "/static/"
            # 和前端约定好，发送网络请求，不管用户名和密码是否验证成功
            # 我都返回同样格式的json对象给你
            # {"code":200,"message":""}

            for k in dic.keys():
                if k == 'Category':
                    if(k!=1) :resul['Category'] = "Wrong"
                    else:resul['Category'] = "CORRECT"
                elif k == 'Situation':
                    if (k!=1): resul['Situation'] = "Wrong"
                    else: resul['Situation'] = "CORRECT"
                if k == 'time':
                    if (k != 1):
                        resul['time'] = "Wrong"
                    else:
                        resul['time'] = "CORRECT"
                elif k == 'Short_term':
                    if (k != 1):
                        resul['Short_term'] = "Wrong"
                    else:
                        resul['Short_term'] = "CORRECT"
                elif k == 'long_time':
                    if (k != 1):
                        resul['long_time'] = "Wrong"
                    else:
                        resul['long_time'] = "CORRECT"
                elif k == 'Note':
                    if (k != 1):
                        resul['Note'] = "Wrong"
                    else:
                        resul['Note'] = "CORRECT"
            for k in resul.keys():print(resul[k])

            # if (re.search('CORRECT$', resul['Category'])
            #         and re.search('CORRECT$', resul['Situation'])
            #         and re.search('CORRECT$', resul['time'])
            #         and re.search('CORRECT$', resul['Short_term'])
            #         and re.search('CORRECT$', resul['long_time'])
            #         and re.search('CORRECT$', ['Note'])
            #
            # ):

            resul['result'] = "INPUT ALL"
            flash('INPUT ALL!')
            return render_template('sell.html')





