from .views import bp
import config
from flask import session,g,render_template
from .models import FrontUser
from apps.models import FollowMessageModel,CommemtMessageModel,DeleteMessageModel,AlertMessageModel
from exts import db

@bp.before_request
def my_before_request():
    if config.FRONT_USER_ID in session:
        user_id = session.get(config.FRONT_USER_ID)
        user = FrontUser.query.get(user_id)
        messages={}
        messages['followmsg']=db.session.query(FollowMessageModel,FrontUser.username).filter(FrontUser.id==FollowMessageModel.content).filter(FollowMessageModel.user_id == user_id).all()
        messages['commentmsg']=db.session.query(CommemtMessageModel,FrontUser.username).filter(FrontUser.id==CommemtMessageModel.content).filter(CommemtMessageModel.user_id == user_id).all()
        messages['deltetmsg']=DeleteMessageModel.query.filter(DeleteMessageModel.user_id == user_id).all()
        messages['alertmsg']=AlertMessageModel.query.filter(AlertMessageModel.user_id == user_id).all()
        if user:
            g.front_user = user
            g.messages= messages


@bp.errorhandler
def page_not_found():
    return render_template('front/front_404.html'),404