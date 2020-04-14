from flask import Blueprint,render_template
notice=Blueprint('notice',__name__)
@notice.route('/notice')
def notices():
    return render_template('website_notice.html')