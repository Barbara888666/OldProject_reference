
from flask import Flask, render_template, request, flash, Blueprint,session,redirect
from util.utils.fileuploads import uploadavatar, uploadalbum, uploaditemimg

sale=Blueprint('sale',__name__)
@sale.route('/sell/', methods=['GET', 'POST'])
def sell_item():
        userid = None
        if 'id' in session:
            userid = session['id']
        if request.method == 'GET':
            if 'id' not in session:
                return redirect('/login')
            return render_template('sell.html')
        else:
            dic = dict(
                Name=request.form.get('Name'),
                Category=request.form.get('Category'),
                Situation=request.form.get('Situation'),
                Price=request.form.get('Price'),
                time=request.form.get('time'),
                Short_term=request.form.get('short time'),
                long_time=request.form.get("long time"),
                Note=request.form.get('Note'),
            )
            f = request.files['pic']
            render_template('sell.html', **dic)
            print(dic)
            print(f.filename is '')
            userid = None
            if 'id' in session:
                userid = session['id']
            if(f.filename!=''):
                uploaditemimg(f,userid)

            flash('PLEASE INPUT ALL!')
            return render_template('sell.html')





