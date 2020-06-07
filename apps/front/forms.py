from ..forms import BaseForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import Regexp, EqualTo, ValidationError, InputRequired
from utils import cache
from .models import FrontUser 
class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='Please enter the correct phonenumber！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{6}",message='Please enter the correct SMS verification!')])
    studentnumber=StringField(validators=[Regexp(r"\w{8}",message='Please enter the correct studentnumber！')])
    username = StringField(validators=[Regexp(r".{2,20}",message='Please enter the correct username！')])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='Please enter the correct password！')])
    password2 = StringField(validators=[EqualTo("password1",message='Entered passwords differ')])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}",message='Please enter the correct graph verification!')])

    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = cache.get(telephone)
        print('1' + sms_captcha_mem)
        if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
            raise ValidationError(message='Message verification error！')


    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        graph_captcha_mem = cache.get(graph_captcha.lower())
        print('1'+graph_captcha)
        print('2'+graph_captcha_mem)
        if not graph_captcha_mem or graph_captcha_mem.lower() != graph_captcha.lower():
            raise ValidationError(message='Graphical verification error！')





class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='Please enter the correct phonenumber！')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='Please enter the correct password！')])
    remeber = StringField()

class AddProductForm(BaseForm):
    # name = StringField(validators=[InputRequired(message='请输入商品名字！')])
    # price = StringField(validators=[InputRequired(message='请输入价格！')])
    # board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])
    # situation = StringField(validators=[InputRequired(message='请输入状况')])
    # term = StringField(validators=[InputRequired(message='请输入时期！')])
    # # term = StringField()
    # description = StringField()
    # # file=FileField(validators=[InputRequired(message='请输入图片！')])
    # file = FileField()
    name = StringField()
    price = StringField()
    board_id = IntegerField()
    situation = StringField()
    term = StringField()
    # term = StringField()
    description = StringField()
    # file=FileField(validators=[InputRequired(message='请输入图片！')])
    file = FileField()

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='Please enter comment content！')])
    product_id = IntegerField(validators=[InputRequired(message='Please enter product ID!')])

class AddLikeForm(BaseForm):
    product_id = IntegerField(validators=[InputRequired(message='Please enter product ID!')])

class AddFollowForm(BaseForm):
    user_id = StringField(validators=[InputRequired(message='Please enter user ID!')])

class SearchForm(BaseForm):
    search = StringField(validators=[InputRequired(message='Please enter search content！')])

class ForgetPasswordForm(BaseForm):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}",message='Please enter the correct phonenumber ！')])
    sms_captcha = StringField(validators=[Regexp(r"\w{6}",message='Please enter the correct SMS verification！')])
    newpassword= StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='Please enter the correct password！')])
    newpassword2 = StringField(validators=[EqualTo("newpassword", message='Entered passwords differ')])
    # password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='Please enter the correct password！')])
    # password2 = StringField(validators=[EqualTo("password1", message='Entered passwords differ')])
    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = cache.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
            raise ValidationError(message='Message verification error！')



