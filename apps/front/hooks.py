from .views import bp
import config
from flask import session,g,render_template
from .models import FrontUser





@bp.errorhandler
def page_not_found():
    return render_template('front/front_404.html'),404