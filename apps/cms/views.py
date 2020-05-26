#encoding: utf-8
import random
import string

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, \
    UpdateBoardForm, AddCmsUserForm
from .models import CMSUser, CMSPermission, cms_role_user,CMSRole
from ..front.models import Product, CommentModel,FrontUser
from .decorators import login_required,permission_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful,cache
from ..models import BannerModel, BoardModel,HighlightProductModel
from tasks import send_mail

bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')

@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    post_list = Product.query.all()
    return render_template('cms/cms_posts.html',products=post_list)

@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    product_id = request.form.get("product_id")
    if not product_id:
        return restful.params_error('请传入商品id！')
    product = Product.query.get(product_id)
    if not product:
        return restful.params_error("没有这个商品！")

    highlight = HighlightProductModel()
    highlight.product = product
    db.session.add(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    product_id = request.form.get("product_id")
    if not product_id:
        return restful.params_error('请传入帖子id！')
    product = Product.query.get(product_id)
    if not product:
        return restful.params_error("没有这篇帖子！")
    highlight = HighlightProductModel.query.filter_by(product_id=product_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/dpost/',methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    product_id = request.form.get("product_id")
    print(product_id)
    if not product_id:
        return restful.params_error('请传入板块id！')
    product = Product.query.get(product_id)
    if not product:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(product)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    comment_models = CommentModel.query.all()
    context = {
        'comments': comment_models
    }
    return render_template('cms/cms_comments.html',**context)

@bp.route('/dcomment/',methods=['POST'])
@login_required
@permission_required(CMSPermission.COMMENTER)
def dcomment():
    comment_id = request.form.get("comment_id")
    print(comment_id)
    if not comment_id:
        return restful.params_error('请传入评论id！')
    comment = CommentModel.query.get(comment_id)
    if not comment:
        return restful.params_error(message='没有这个评论！')

    db.session.delete(comment)
    db.session.commit()
    return restful.success()

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error('请传入板块id！')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()

@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    front_usermodels = FrontUser.query.all()
    context = {
        'front_users': front_usermodels
    }
    return render_template('cms/cms_fusers.html',**context)

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    cmsusers = CMSUser.query.all()
    context = {
        'cmsusers': cmsusers
    }
    return render_template('cms/cms_cusers.html',**context)

@bp.route('/acmsuser/',methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def addcusers():
    form = AddCmsUserForm(request.form)
    if form.validate():
        email = form.email.data
        emialkey=CMSUser.query.filter(CMSUser.email==email).first()
        #user = FrontUser.query.filter(FrontUser.telephone==telephone)
        print(emialkey)
        if emialkey:
            return restful.params_error('该用户已存在！')
        else:
            username = form.username.data
            permission=form.permission.data
            print(email)
            print(permission)
            password='12345678'
            user = CMSUser(email=email, username=username,password=password)
            db.session.add(user)
            db.session.commit()
            if not permission:
                permission='Visitor'
            user = CMSUser.query.filter_by(email=email).first()
            if user:
                role = CMSRole.query.filter_by(name=permission).first()
                if role:
                    role.users.append(user)
                    db.session.commit()
                    print('User to be a Role Success！')
                else:
                    print('No this Role：%s' % role)
            else:
                print('%s no register!' % email)
            # permisstmp=cms_role_user(cms_role_id=per,cms_user_id=idtmp)
            # db.session.add(permisstmp)
            # db.session.commit()
            return restful.success()
    else:
        return restful.params_error(message=form.get_error())
    return render_template('cms/cms_cusers.html')



@bp.route('/banners/')
@login_required
def banners():
    # banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    # return render_template('cms/cms_banners.html',banners=banners)
    return render_template('cms/cms_banners.html',banners=banners)

@bp.route('/abanner/',methods=['POST'])
@login_required
def abanner():
    form=AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/dbanner/',methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()

@bp.route('/email_captcha/')
def email_captcha():
    email=request.args.get('email')
    if not email:
        return restful.params_error('Please input the correct Email')
    print(email)
    source= list(string.ascii_letters)
    # source.extend(list(range(0,10)))
    source.extend(map(lambda x:str(x),range(0,10)))
    # source.extend(['0','1','2','3','4','5','6','7','8','9'])
    captcha=''.join(random.sample(source,6))
    # message =Message('BJUT Second Market Email Confirm',recipients=[email]
    #                  ,body='Your Email Code is : %s' %captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    send_mail.delay('BJUT Second Market Email Confirm', [email], 'Your Email Code is : %s' % captcha)
    cache.set(email,captcha)
    return restful.success()

@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')




class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # if session.permanent = True
                    # the date is 31 days
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='Email or Password is Wrong')
        else:
            message = form.get_error()
            return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code":200,message=""}
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("The Old Password is Wrong")
        else:
            return restful.params_error(form.get_error())
# app(iOS/Andorid)

class ResetEmailView(views.MethodView):
    decorator=[login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form=ResetEmailForm(request.form)
        if form.validate():
            email=form.email.data
            g.cms_user.email=email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))