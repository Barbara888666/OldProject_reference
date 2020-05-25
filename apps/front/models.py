import enum
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
import shortuuid

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    studentnumber = db.Column(db.String(50),nullable=False,unique=True)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50),unique=True)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(FrontUser, self).__init__(*args,**kwargs)


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)

class SituationEnum(enum.Enum):
    Brand_new = 1
    Slightly_used = 2
    Used = 3
    Left_over = 4

class TermEnum(enum.Enum):
    Emergency= 1
    Short_term = 2
    Long_term = 3


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    price = db.Column(db.FLOAT,default=9.9)
    name = db.Column(db.String(100),default='productname')
    picture = db.Column(db.String(100))
    description = db.Column(db.String(100),default='')
    situation = db.Column(db.Enum(SituationEnum),default=SituationEnum.Slightly_used)
    term = db.Column(db.Enum(TermEnum),default=TermEnum.Long_term)
    join_time = db.Column(db.DateTime,default=datetime.now)

    board_id = db.Column(db.INTEGER, db.ForeignKey('board.id'))
    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))
    board = db.relationship("BoardModel", backref="products")
    user = db.relationship("FrontUser", backref='products')

class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content =db.Column(db.String(200))
    create_time = db.Column(db.DateTime,default=datetime.now)

    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    commenter_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    product = db.relationship("Product", backref="comments")
    commenter = db.relationship("FrontUser", backref='comments')

class LikeModel(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    liker_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    product = db.relationship("Product", backref="likes")
    liker = db.relationship("FrontUser", backref='likes')


