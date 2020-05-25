from ..forms import BaseForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import Regexp, EqualTo, ValidationError, InputRequired
from utils import cache
from .models import FrontUser

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式的手机号码！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{6}",message='请输入正确格式的短信验证码！')])
    studentnumber=StringField(validators=[Regexp(r"\w{8}",message='请输入正确格式的学号！')])
    username = StringField(validators=[Regexp(r".{2,20}",message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1",message='两次输入的密码不一致！')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='请输入正确格式的短信验证码！')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = cache.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
            raise ValidationError(message='短信验证码错误！')


    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        graph_captcha_mem = cache.get(graph_captcha.lower())
        print('1'+graph_captcha)
        print('2'+graph_captcha_mem)
        if not graph_captcha_mem or graph_captcha_mem.lower() != graph_captcha.lower():
            raise ValidationError(message='图形验证码错误！')





class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='请输入正确格式的手机号码！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    remeber = StringField()

class AddProductForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入商品名字！')])
    price = StringField(validators=[InputRequired(message='请输入价格！')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])
    situation = StringField(validators=[InputRequired(message='请输入状况')])
    term=StringField(validators=[InputRequired(message='请输入时期！')])
    description = StringField()
    file= FileField()


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    product_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])

class AddLikeForm(BaseForm):
    product_id = IntegerField(validators=[InputRequired(message='请输入帖子id！')])

class ForgetPasswordForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='请输入正确格式的手机号码！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{6}",message='请输入正确格式的短信验证码！')])


    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = cache.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
            raise ValidationError(message='短信验证码错误！')



