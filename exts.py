#encoding: utf-8

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.SMS import SMS

db = SQLAlchemy()
mail =Mail()
sms = SMS()