import os
from flask import render_template, request, flash, Blueprint


sale=Blueprint('sale',__name__)
@sale.route('/sell/', methods=['GET', 'POST'])
def sell_item():
        if request.method == 'GET':
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
            print(f.filename is None)


                # basepath = os.path.dirname(__file__)  # 当前文件所在路径
                # print(basepath)
                # from werkzeug.utils import secure_filename
                # upload_path = os.path.join(basepath, 'upload_file_dir', secure_filename(f.filename))
                # # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                # print(upload_path)
                # upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径
                # print(upload_path)
                # f.save(upload_path)



            flash('PLEASE INPUT AS MORE!')
            return render_template('sell.html')





