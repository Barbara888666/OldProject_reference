from flask import Blueprint,render_template
popular=Blueprint('popular',__name__)
@popular.route('/popular')
def populars():
    return render_template('popular_products.html')