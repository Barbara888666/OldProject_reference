#encoding: utf-8
import os

SECRET_KEY = 'liangluya'

imgpath=os.path.join(os.getcwd(),'static','imgs')

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'myself'

# PERMANENT_SESSION_LIFETIME =

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


# WTF_CSRF_CHECK_DEFAULT=False
CMS_USER_ID = 'ALWAYSLLY'
FRONT_USER_ID ='ALLPEOPLE'

# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
# MAIL_SERVER = "smtp.qq.com"
MAIL_SERVER = "smtp.163.com" #发送的邮箱 sender email
# MAIL_PORT = '994'465/994
# MAIL_USE_TLS = True
MAIL_PORT = '465'
MAIL_USE_SSL = True
MAIL_USERNAME = "19801355517@163.com"
MAIL_PASSWORD = "BPJCEFVGQNRXQRFQ"
MAIL_DEFAULT_SENDER = "19801355517@163.com"

# 阿里云相关配置

# ACCESS_KEY_ID = 'LTAI4GGHqEYTr4kTiHfQNCNX'  #用户AccessKey  需要根据自己的账户修改 LTAI4GGHqEYTr4kTiHfQNCNX
# ACCESS_KEY_SECRET = 'Vjp6OJiw6ewJgGB9hOmAKAQuZz0XRq'
# SIGN_NAME_FIELD = 'SecondMarket'
# TEMPLATE_CODE_FIELD = 'SMS_190272838'

ACCESS_KEY_ID = 'LTAI4GBFPiYKhAZA6jiSjR7g'  #用户AccessKey  需要根据自己的账户修改 LTAI4GGHqEYTr4kTiHfQNCNX
ACCESS_KEY_SECRET = 'h9259qKhGmnSDLHnpD2njTujLDqQTf'
SIGN_NAME_FIELD = 'SecondMarket'
TEMPLATE_CODE_FIELD = 'SMS_190272838'


#flask_paginate的相关配置
PER_PAGE=6
# celery相关的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"