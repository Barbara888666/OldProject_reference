from apps.forms import BaseForm
from wtforms import StringField,ValidationError
from wtforms.validators import regexp,InputRequired
import hashlib
from ..front.models import FrontUser

class SMSCaptchaForm(BaseForm):
    salt = 'q3423805gdflvbdfvhsdoa`#$%'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])
    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest()
        print('客户端提交的sign：',sign)
        print('服务器生成的sign：',sign2)
        if sign == sign2:
            user = FrontUser.query.filter_by(telephone=telephone).count()
            print(user)
            if user != 0:
                return False
            else:
                return True
        else:
            return False


class SMSCaptchaForm2(BaseForm):
    salt = 'q2458805182gdflvbdfvhsdoa`#$%'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    # def validate_repeat(self):
    #     result = super(SMSCaptchaForm, self).validate_repeat()
    #     if not result:
    #         return False
    #     print("自定义验证函数-手机号")
    #     telephone = self.telephone.data
    def validate(self):
        result = super(SMSCaptchaForm2, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(timestamp+telphone+salt)
        # md5函数必须要传一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        print('客户端提交的sign：', sign)
        print('服务器生成的sign：', sign2)
        if sign == sign2:
            user = FrontUser.query.filter_by(telephone=telephone).count()
            if user == 0:
                return False
            else:
                return True
        else:
            return False
