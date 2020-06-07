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
    oldpwd = StringField(validators=[Length(6,20,message='Please enter the old password in the correct format')])
    newpwd = StringField(validators=[Length(6,20,message='Please enter the new password in the correct format')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='Confirm the new password')])

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
    name = StringField(validators=[InputRequired(message='Please enter the banner name！')])
    image_url = StringField(validators=[InputRequired(message='Please enter the banner link！')])
    link_url = StringField(validators=[InputRequired(message='Please enter the banner url link！')])
    priority = IntegerField(validators=[InputRequired(message='Please enter the banner priority！')])

class UpdateBannerForm(BaseForm):
    banner_id = IntegerField(validators=[InputRequired(message='Please enter the banner id！')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='Please enter the banner name！')])

class UpdateBoardForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message='Please enter the banner id！')])

class WarnUserForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message='Please enter the user id！')])

class AddCmsUserForm(BaseForm):
    email = StringField(validators=[InputRequired(message='Please enter the CMS user email！')])
    username = StringField(validators=[InputRequired(message='Please enter the CMS user username！')])
    permission = StringField()
