from flask import Blueprint, make_response, request, jsonify
from qiniu import put_data

from utils.captcha import Captcha
from utils import cache
from io import BytesIO
from exts import sms
from utils import restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm, SMSCaptchaForm2
import random
import qiniu
from tasks import send_sms_captcha


bp = Blueprint("common",__name__,url_prefix='/c')


@bp.route('/')
def index():
    return 'common index'

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    cache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # ?telephone=xxx
#     # /c/sms_captcha/xxx
#     telephone = request.args.get('telephone')
#     captcha=Captcha.gene_text(number=6)
#     result=sms.send(telephone,code=captcha)
#     if result :
#         return restful.success()
#     else :
#         return restful.params_error(message="The code is Wrong!")

@bp.route('/sms_captcha/',methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = ''.join(str(i) for i in random.sample(range(0, 9), 6))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
        print('发送的短信是'+captcha)
        if sms.send(telephone,code=captcha):
            cache.set(telephone,captcha)
            print('发送成了')
            return restful.success()
        else:
            return restful.params_error()
            # cache.set(telephone,captcha)
            # return restful.success()
    else:
        return restful.params_error(message='Parameter error！')

@bp.route('/sms_captcha2/',methods=['POST'])
def sms_captcha2():
    form = SMSCaptchaForm2(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = ''.join(str(i) for i in random.sample(range(0, 9), 6))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
        # captcha = Captcha.gene_text(number=6)
        print('SMS froget password message verification code：',captcha)
        # if sms.send(telephone,code=captcha):
        # if send_sms_captcha.delay(telephone, captcha):
        # if 1==1:
        if sms.send(telephone,code=captcha):
            cache.set(telephone,captcha)
            print('发送成了')
            return restful.success()
        else:
            return restful.params_error()
            # cache.set(telephone,captcha)
            # return restful.success()
    else:
        return restful.params_error(message='Parameter error！')

@bp.route('/uptoken/')
def uptoken(inputdata):
    access_key = 'Uwq02H2kU4TvcdGe4S59EJL50P14u6sNbgrueM0n'
    secret_key = 'G1V1HiPuZurs8KaHnJHIsDZ1u-ub1b2191UkC7UA'
    q = qiniu.Auth(access_key,secret_key)
    bucket = 'liangluya'
    token = q.upload_token(bucket)

    ret1, ret2 = put_data(token, None, data=inputdata)
    print('ret1:', ret1)
    print('ret2:', ret2)

    if ret2.status_code != 200:
        raise Exception('File upload failed')

    return ret1.get('key')

    # return jsonify({'uptoken':token})