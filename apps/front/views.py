#encoding: utf-8
import os

from flask import Blueprint, views, request, render_template, url_for, session, g, abort, jsonify, redirect
from sqlalchemy import func

from apps.front.forms import SignupForm, SigninForm, AddProductForm, AddCommentForm, ForgetPasswordForm, AddLikeForm
from exts import sms,db
from utils import restful,safeutils
from utils.captcha import Captcha
from .models import FrontUser, Product, CommentModel, LikeModel
import config
from ..models import BannerModel, BoardModel, HighlightProductModel, MessageModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from tasks import send_sms_captcha
from ..common.views import uptoken
# from werkzeug.utils import secure_filename

bp = Blueprint("front",__name__)


@bp.route('/change')

def change():
    return render_template('front/htmls/change_information.html')

@bp.route('/detail/')
def details():
    return render_template('front/htmls/商品详情.html')

@bp.route('/emerge')
def emerges():
    return render_template('front/htmls/emerge.html')
#买列表：想买的物品，描述，买家名字
#卖列表：商品图片，商品名字，分类，卖家名字

@bp.route('/favorites')
def favorite():
    return render_template('front/htmls/favorites.html')

@bp.route('/highpre')
def highpres():
    return render_template('front/htmls/high_predibility_seller.html')
#搜索网站通知列表

@bp.route('/')
def main_page():
    if session[config.FRONT_USER_ID]:
        userid=g.front_user.id
        return render_template('front/htmls/main_page.html',userid=userid)
    else:
        return render_template('front/htmls/main_page.html')

@bp.route('/news')
def new():
    return render_template('front/htmls/my_news.html')
#有多少人想联系我、有多少人收藏我的物品

@bp.route('/notice')
def notices():
    return render_template('front/htmls/website_notice.html')
#搜索网站通知列表

@bp.route('/personal')
@login_required
def personals():
    # userid = g.front_user.id
    t = g.front_user.id
    # username = t[0][0]
    # email = t[0][1]
    # phone = t[0][2]
    # return render_template('front/htmls/personal_information.html', username=username, email=email, phone=phone)
    return render_template('front/htmls/personal_information.html')



@bp.route('/popular')
def populars():
    return render_template('front/htmls/popular_products.html')
#商品名字，商品图片，卖家

# @search.route('/search',classmethod=('GET','POST'))
# def searchtest():
#     #由后端传送文件的示范
#     file="/images/test.jpg"
#     return render_template('search_web_page.html',file=file)
@bp.route('/search')
def searchtest():
    return render_template('front/htmls/search_web_page.html')
@bp.route('/testsearch/')
def searchs():
    return render_template('front/htmls/testsearch.html')
#搜索分类列表及分类物品
#物品列表：物品id，物品图片，物品名，卖家名字，卖家信誉度，物品介绍信息
#更换排序（名字，卖家信誉度，买家喜爱度（可取舍该功能）

@bp.route('/testmain/')
@login_required
def tests():
    t = g.front_user.id
    # a = searchitems()
    # img=searchavatar(int(session['id'])
    # album = searchalbum(int(session['id'])
    #
    # itemimg =searchitemimg()
    username = t[0][0]
    email = t[0][1]
    phone = t[0][2]
    return render_template('front/htmls/maintest.html', username=username, email=email, phone=phone)

#卖家信息：卖家名字，卖家个人介绍，卖家信誉度，卖家qq、微信、电话
#卖家商品列表：商品图片，商品名字，商品分类





































@bp.route('/a')
def index():
    board_id=request.args.get('bd',type=int,default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    # products = Product.query.all()
    sort=request.args.get('st',type=int,default=1)
    query_obj = None
    print(sort)
    if sort == 1:
        #添加的时间排序
        query_obj = Product.query.order_by(Product.join_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(Product).outerjoin(HighlightProductModel).order_by(
            HighlightProductModel.create_time.desc(), Product.join_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = Product.query.order_by(Product.like.desc())
    elif sort == 4:
        # 按照价格便宜排序
        query_obj = Product.query.order_by(Product.price.asc())

    page = request.args.get(get_page_parameter(), type=int, default=1)
    start=(page-1)*config.PER_PAGE
    end=start+config.PER_PAGE
    products = None
    total = None
    if (board_id!=0):
        # products_obj = Product.query.filter_by(board_id=board_id)
        products_obj = query_obj.filter(Product.board_id  == board_id)
        products=products_obj.slice(start, end)
        total = products_obj.count()
    else:
        products = query_obj.slice(start, end)
        total=Product.query.count()
    pagination = Pagination(bs_version=3,page=page,total=total)
    context = {
        'banners': banners,
        'boards': boards,
        'products':products,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort': sort,
    }
    return render_template('front/front_index2.html', **context)


@bp.route('/logout/')
@login_required
def logout():
    del session[config.FRONT_USER_ID]
    return redirect(url_for('front.signin'))

# @bp.route('/forget_password/')
# def forget_password():
#
#     return render_template('front/front_forget_password.html')

class Forget_password(views.MethodView):
    def get(self):
        return render_template('front/front_forget_password.html')

    def post(self):
        form = ForgetPasswordForm(request.form)
        if form.validate():
            telephone= form.telephone.data
            print(telephone)
            user = FrontUser.query.filter(FrontUser.telephone==telephone).first()
            print(user)
            db.session.delete(user)
            db.session.commit()
            print("delete success")
            return restful.success("confirm success")
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())
bp.add_url_rule('/forget_password/',view_func=Forget_password.as_view('forget_password'))

@bp.route('/t/<user_id>')
def ta_page(user_id):
    ta = FrontUser.query.get(user_id)
    if not ta:
        abort(404)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    products_obj = Product.query.order_by(Product.join_time.desc())
    products_obj = products_obj.filter_by(user_id =user_id)
    products=products_obj.slice(start, end)
    total = products_obj.count()

    pagination = Pagination(bs_version=3,page=page,total=total)
    context = {
        'ta': ta,
        'products':products,
        'pagination':pagination,
    }
    return render_template('front/front_tapage.html', **context)

@bp.route('/p/<product_id>')
def product_detail(product_id):
    product=Product.query.get(product_id)
    print(product.user)
    # user_id=product.user.id
    like=LikeModel.query.filter(LikeModel.product_id==product_id).filter(LikeModel.liker==g.front_user).first()
    # query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
    # like=LikeModel.query.get(product_id)
    # like=like.filter_by(user_id=user_id)
    print(like)
    if not product:
        abort(404)
    if not like:
        like=0
    else:
        like=1
    return render_template('front/front_product_detail.html',product=product,like=like)


@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        product_id = form.product_id.data
        product = Product.query.get(product_id)
        if product:
            comment = CommentModel(content=content)
            comment.product = product
            comment.commenter= g.front_user
            producttmp = Product.query.filter(Product.id == product_id).first()
            if not producttmp.comment:
                producttmp.comment = 0
            producttmp.comment = producttmp.comment + 1
            content="You are followed by ssss"
            message=MessageModel(content=content,user_id=product.user_id,type='comment')
            db.session.add(comment)
            db.session.add(message)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())

@bp.route('/alike/',methods=['POST'])
@login_required
def add_like():
    form = AddLikeForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        print(product_id)
        print("             id+")
        product = Product.query.get(product_id)
        print(product)
        if product:
            like = LikeModel()
            like.product = product
            like.liker = g.front_user
            producttmp = Product.query.filter(Product.id == product_id).first()
            if not producttmp.like:
                producttmp.like=0
            producttmp.like = producttmp.like+1
            content = "You are liked by ssss"
            message = MessageModel(content=content, user_id=product.user_id, type='like')
            db.session.add(message)
            db.session.add(like)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            studentnumber = form.studentnumber.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password,studentnumber=studentnumber)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())
bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))

class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html',return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remeber.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))



@bp.route('/aproduct/',methods=['GET','POST'])
@login_required
def aproduct():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_aproduct3.html',boards=boards)
    else:
        f = request.files.get('pic','')
        if (f != None):
            basepath = os.path.dirname(__file__)
            print(basepath)
            # upload_path = os.path.join(basepath, 'upload_file_dir', secure_filename(f.filename))
            # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            # print(upload_path)
            # upload_path = os.path.abspath(upload_path)  # 将路径转换为绝对路径
            # print(upload_path)
            # f.save(upload_path)
        form = AddProductForm(request.form)
        if form.validate():
              name = form.name.data
              price = form.price.data
              board_id = form.board_id.data
              board = BoardModel.query.get(board_id)
              situstion = form.situation.data
              term = form.term.data
              description = form.description.data


              if not board:
                 return restful.params_error(message='没有这个板块！')
              product = Product(name=name,price=price,board_id=board_id,situation=situstion,term=term,description=description,like=0,comment=0)
              product.board = board
              product.user_id = g.front_user.id
              product.user = g.front_user
              db.session.add(product)
              db.session.commit()
              return restful.success()
        else:
            return restful.params_error(message=form.get_error())




