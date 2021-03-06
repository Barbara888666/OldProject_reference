import enum

from exts import db
from datetime import datetime

class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    image_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(1023),nullable=False)
    priority = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)

class HighlightProductModel(db.Model):
    __tablename__ = 'highlight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)

    product = db.relationship("Product", backref="highlight")


class FollowMessageModel(db.Model):
    __tablename__ = 'follow_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    #srcuser = db.relationship("FrontUser", backref="follow_messages_src",foreign_keys=user_id)
    #desuser = db.relationship("FrontUser", backref="follow_messages_des",foreign_keys=content)
    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content


class CommemtMessageModel(db.Model):
    __tablename__ = 'comment_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    pid=db.Column(db.Integer,db.ForeignKey('product.id'))
    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))
    srcuser = db.relationship("FrontUser", backref="follow_messages_src",foreign_keys=user_id)
    desuser = db.relationship("FrontUser", backref="follow_messages_des",foreign_keys=content)
    def __init__(self, user_id, content,pid):
        self.user_id = user_id
        self.content = content
        self.pid=pid 

class DeleteMessageModel(db.Model):
    __tablename__ = 'delete_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    #srcuser = db.relationship("FrontUser", backref="follow_messages_src",foreign_keys=user_id)
    #target = db.relationship("product", backref="follow_messages_tar",foreign_keys=content)

class AlertMessageModel(db.Model):
    __tablename__ = 'alert_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    User = db.relationship("FrontUser", backref="alert_messages")    
