
from flask import Flask, render_template, request, flash, Blueprint,session,redirect
from db.upload import uploaditem
sale=Blueprint('sale',__name__,static_folder='static')
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
                Note=request.form.get('Note'),
            )
            f = request.files.get('pic','')
            render_template('sell.html', **dic)
            userid = None
            if 'id' in session:
                userid = session['id']
            if(f==''):
                f=None
            uploaditem(dic['Name'],userid,dic['Note'],dic['Category'],float(dic['Price']),True,dic['Situation'],f)
            flash('PLEASE INPUT ALL!')
            return redirect('/')





