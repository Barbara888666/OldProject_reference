from flask import Blueprint,render_template
emerge=Blueprint('emerge',__name__)
@emerge.route('/emerge')
def emerges():
    return render_template('emerge.html')