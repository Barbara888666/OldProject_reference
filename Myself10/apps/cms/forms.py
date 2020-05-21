#encoding: utf-8
from flask import g
from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import cache
from wtforms import ValidationError

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='Please input the correct Email'),
                                    InputRequired(message='Please input the Email')])
    password = StringField(validators=[Length(6,20,message='Please input the correct Password')])
    remember=IntegerField()



class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='确认密码必须和新密码保持一致')])

class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='Please input the correct Email'),
                                    InputRequired(message='Please input the Email')])
    captcha= StringField(validators=[Length(min=6,max=6,message='Length of Code is Wrong')])

    def validate_captcha(self, field):
        captcha=field.data
        email=self.email.data
        captcha_cache=cache.get(email)
        if not captcha_cache or captcha.lower()!=captcha_cache.lower():
            raise ValidationError('Email Confirm Fail!')

    def validate_email(self,field):
        email=field.data
        user =g.cms_user
        if user.email==email:
            raise ValidationError('Can not Change to the Same Email!')

# class ResetEmailForm(BaseForm):
#     email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
#     captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])
#
#     def validate_captcha(self,field):
#         captcha = field.data
#         email = self.email.data
#         captcha_cache = cache.get(email)
#         if not captcha_cache or captcha.lower() != captcha_cache.lower():
#             raise ValidationError('邮箱验证码错误！')
#
#     def validate_email(self,field):
#         email = field.data
#         user = g.cms_user
#         if user.email == email:
#             raise ValidationError('不能修改为相同的邮箱！')
class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])



