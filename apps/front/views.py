#encoding: utf-8
import os

from flask import Blueprint, views, request, render_template, url_for, session, g, abort, jsonify, redirect
from sqlalchemy import func
from werkzeug.utils import secure_filename

from apps.front.forms import SignupForm, SigninForm, AddProductForm, AddCommentForm, ForgetPasswordForm, AddLikeForm, \
    AddFollowForm
from exts import sms,db
from utils import restful,safeutils,uploadproductimgs
from utils.captcha import Captcha
from .models import FrontUser, Product, CommentModel, LikeModel, FollowModel, product_imgs
import config
from ..models import BannerModel, BoardModel, HighlightProductModel, FollowMessageModel,CommemtMessageModel
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from tasks import send_sms_captcha
from ..common.views import uptoken
from apps.front.models import product_imgs
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

@bp.route('/a')
def main_page():
    if config.FRONT_USER_ID in session:
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

@bp.route('/s/',methods=['POST'])
def s():
    if request.method=='POST':
        s=request.forms.get('search','')
        if s!='':
            return redirect('/search/'+s)
    abort(404)

@bp.route('/search/<content>')
def searchss(content):
    board_id = request.args.get('bd', type=int, default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    # products = Product.query.all()
    sort = request.args.get('st', type=int, default=1)
    print(sort)
    query_obj = db.session.query(Product, product_imgs).outerjoin(product_imgs).filter(product_imgs.seq == 0).filter(Product.name==content)
    if sort == 1:
        # 添加的时间排序
        query_obj = query_obj.order_by(Product.join_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = query_obj.order_by(
            HighlightProductModel.create_time.desc(), Product.join_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = query_obj.order_by(Product.like.desc())
    elif sort == 4:
        # 按照价格便宜排序
        query_obj = query_obj.order_by(Product.price.asc())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    products = None
    total = None
    if board_id:
        # products_obj = Product.query.filter_by(board_id=board_id)
        products_obj = query_obj.filter(Product.board_id == board_id)
        products = products_obj.slice(start, end)
        total = products_obj.count()
    else:
        products = query_obj.slice(start, end)
        total = query_obj.count()
    # 调用imglink的示例
    # print(products[0][1].imglink) imglink换成seq
    # 调用product的示例: products[0][0].x
    pagination = Pagination(bs_version=3, page=page, total=total)
    context = {
        'banners': banners,
        'boards': boards,
        'products': products,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort,
    }
    return render_template('front/front_search.html',**context)
@bp.route('/personal/',methods=['GET','POST'])
@login_required
def searchp():
    user=FrontUser.query.filter(FrontUser.id==g.front_user.id).first()
    userproducts=db.session.query(Product.name,Product.id,product_imgs,BoardModel.name).outerjoin(product_imgs,BoardModel).filter(Product.user_id==g.front_user.id).filter(product_imgs.seq==0).all()
    print(userproducts)
    return render_template('front/front_personal.html',user=user,gender=str(user.gender).strip('GenderEnum.'),product=userproducts)

@bp.route('/changeinfo/',methods=['POST'])
@login_required
def changeinfo():
    name=request.form.get('uname','')
    email=request.form.get('email','')
    gender=request.form.get('gender','')
    signature=request.form.get('des','')
    avatar=request.files.get('file','')
    info={}
    if name!='':
        info.update({'username':name})
    if email!='':
        info.update({'email':email})
    if gender!='':
        info.update({'gender':gender})
    if signature!='':
        info.update({'signature':signature})
    if avatar!='':
        info.update({'avatar':avatar})
    if info!={}:
        FrontUser.query.filter(FrontUser.id==g.front_user.id).update(info).commit()
    return jsonify("success")

@bp.route('/category/')
def index():
    board_id=request.args.get('bd',type=int,default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()

    # products = Product.query.all()
    sort=request.args.get('st',type=int,default=1)
    print(sort)
    if sort == 1:
        #添加的时间排序
        query_obj = db.session.query(Product,product_imgs).outerjoin(product_imgs).filter(product_imgs.seq==0).order_by(Product.join_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(Product,product_imgs).outerjoin(HighlightProductModel).outerjoin(product_imgs).filter(product_imgs.seq==0).order_by(
            HighlightProductModel.create_time.desc(), Product.join_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = db.session.query(Product,product_imgs).filter(product_imgs.seq==0).order_by(Product.like.desc())
    elif sort == 4:
        # 按照价格便宜排序
        query_obj = db.session.query(Product,product_imgs).filter(product_imgs.seq==0).order_by(Product.price.asc())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start=(page-1)*config.PER_PAGE
    end=start+config.PER_PAGE
    products = None
    total = None
    if board_id:
        # products_obj = Product.query.filter_by(board_id=board_id)
        products_obj = query_obj.filter(Product.board_id  == board_id)
        products=products_obj.slice(start, end)
        total = products_obj.count()
    else:
        products = query_obj.slice(start, end)
        total = query_obj.count()
    #调用imglink的示例
    #print(products[0][1].imglink) imglink换成seq
    #调用product的示例: products[0][0].x
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

# @bp.route('/message/')
# @login_required
# def message():
#     messages=MessageModel.query.filter(MessageModel.user_id==g.front_user.id)
#     print(g.messages)
#     return render_template('front/front_message.html',messages=messages)

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
    ta = FrontUser.query.filter(FrontUser.id==user_id).first()
    if not ta:
        abort(404)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    products_obj = Product.query.order_by(Product.join_time.desc()).filter_by(user_id =user_id)
    products=products_obj.join(product_imgs,Product.id==product_imgs.pid).slice(start, end)
    #b=Follow.query.join(Post,Follow.followed_id==Post.author_id).filter(Follow.follower_id==2)
    total = products_obj.count()
    follow=0
    if config.FRONT_USER_ID in session:
        follow=FollowModel.query.filter(FollowModel.follower==g.front_user).filter(FollowModel.star==ta).first()
    pagination = Pagination(bs_version=3,page=page,total=total)
    context = {
        'ta': ta,
        'products':products,
        'pagination':pagination,
        'follow':follow
    }
    return render_template('front/front_tapage.html', **context)

@bp.route('/p/<product_id>')
def product_detail(product_id):
    product=Product.query.get(product_id)
    pimgs=product_imgs.query.filter(product_imgs.pid==product_id).order_by(product_imgs.seq).all()
    like=0
    if config.FRONT_USER_ID in session:
        like=LikeModel.query.filter(LikeModel.product_id==product_id).filter(LikeModel.liker==g.front_user).first()
    if not product:
        abort(404)
    return render_template('front/front_product_detail.html',product=product,like=like,productimgs=pimgs)


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
            content = "Your product %s is commented by %s" % (product.name, comment.commenter.username)
            # content="Your product %s is commented by %s",product.name,comment.commenter.username
            message=CommemtMessageModel(content=comment.commenter.id,user_id=product.user_id)
            db.session.add(comment)
            db.session.add(message)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())

@bp.route('/dcomment/',methods=['POST'])
@login_required
def dcomment():
    comment_id = request.form.get("comment_id")
    comment=CommentModel.query.get(comment_id)
    product=comment.product.id
    producttmp = Product.query.filter(Product.id == product).first()
    if not producttmp.comment:
        producttmp.comment = 0
    producttmp.comment = producttmp.comment -1
    db.session.delete(comment)
    db.session.commit()
    return restful.success()

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
            db.session.add(like)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())
@bp.route('/dlike/',methods=['POST'])
@login_required
def dlike():
    like_id = request.form.get("like_id")
    print(like_id)
    like=LikeModel.query.get(like_id)
    print(like)
    product=like.product.id
    producttmp = Product.query.filter(Product.id == product).first()
    if not producttmp.like:
        producttmp.like = 0
    producttmp.like = producttmp.like -1
    db.session.delete(like)
    db.session.commit()
    return restful.success()

@bp.route('/afollow/',methods=['POST'])
@login_required
def add_follow():
    form = AddFollowForm(request.form)
    if form.validate():
        user_id = form.user_id.data
        print(user_id)
        print("             id+")
        user = FrontUser.query.get(user_id)
        print(user)
        if user:
            follow = FollowModel()
            follow.follower = g.front_user
            startmp = FrontUser.query.filter(FrontUser.id == user_id).first()
            follow.star=startmp
            content = "You are followed by %s" %follow.follower.username
            message = FollowMessageModel(content=follow.follower.id, user_id=startmp.id, type='follow')
            db.session.add(message)
            db.session.add(follow)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这个用户！')
    else:
        return restful.params_error(form.get_error())

@bp.route('/dfollow/',methods=['POST'])
@login_required
def dfollow():
    follow_id = request.form.get("follow_id")
    print(follow_id)
    follow=FollowModel.query.get(follow_id)
    print(follow)
    db.session.delete(follow)
    db.session.commit()
    return restful.success()


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
            # return redirect(url_for('front.signin'))
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
        print('success')
        print(request)
        f = request.files.getlist('file')
        print(f)
        name = request.form['name']
        print(name)
        price = request.form['price']
        print(price)
        board_id = request.form['board_id']
        print(board_id)
        situation = request.form['situation']
        print(situation)
        term = request.form['term']
        print(term)
        description = request.form['description']
        print(description)
        board = BoardModel.query.get(board_id)
        product = Product(name=name, price=price, board_id=board_id, situation=situation, term=term,
                          description=description, like=0, comment=0)
        product.board = board
        product.user_id = g.front_user.id
        product.user = g.front_user
        db.session.add(product)
        db.session.commit()
        name = request.form['name']
        print('name')
        # postdata = request.form['name']
        # print(postdata)
        price = request.form['price']
        f = request.files.getlist('file')
        board_id = request.form['board_id']
        situation=request.form['situation']
        term=request.form['term']
        description=request.form['description']
        product = Product(name=name,price=price,board_id=board_id,situation=situation,term=term,description=description,like=0,comment=0)
        product.user = g.front_user
        product.user_id = g.front_user.id
        db.session.add(product)
        db.session.commit()
        pid=product.id
        if not f==[]:
            r=uploadproductimgs(f,pid)
            for t,seq in zip(r,range(0,len(r))):
                pimg=product_imgs(pid=pid,imglink=t,seq=seq)
                db.session.add(pimg)
        else:
            pimg=product_imgs(pid=pid,imglink='none',seq=0)
            db.session.add(pimg)       
        db.session.commit() 
        return  jsonify('succcess')
        # else/
        #       return restful.params_error(message=form.get_error())
# bp.add_url_rule('/aproduct/',view_func=aproductView.as_view('aproduct'))



