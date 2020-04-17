from flask import Blueprint,render_template
login=Blueprint('login',__name__)
@login.route('/login')
def logins():
    return render_template('/login.html')