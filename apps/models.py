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

    User = db.relationship("FrontUser", backref="messages")

class CommemtMessageModel(db.Model):
    __tablename__ = 'comment_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100),db.ForeignKey('front_user.id'),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    User = db.relationship("FrontUser", backref="messages")

class DeleteMessageModel(db.Model):
    __tablename__ = 'delete_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    User = db.relationship("FrontUser", backref="messages")

class AlertMessageModel(db.Model):
    __tablename__ = 'alert_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(100), db.ForeignKey("front_user.id"))

    User = db.relationship("FrontUser", backref="messages")    