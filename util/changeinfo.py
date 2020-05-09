from flask import Blueprint,render_template
changeinfo=Blueprint('changeinfo',__name__)
@changeinfo.route('/change')
def change():
    return render_template('change_information.html')
