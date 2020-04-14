from flask import Blueprint,render_template
favorites=Blueprint('favorites',__name__)
@favorites.route('/favorites')
def favorite():
    return render_template('favorites.html')
