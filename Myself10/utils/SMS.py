import logging

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import config

class SMS:
    SIGN_NAME_FIELD = config.SIGN_NAME_FIELD
    TEMPLATE_CODE_FIELD = config.TEMPLATE_CODE_FIELD
    ACCESS_KEY_ID = config.ACCESS_KEY_ID  # 用户AccessKey  需要根据自己的账户修改
    ACCESS_KEY_SECRET = config.ACCESS_KEY_SECRET # Access Key Secret  需要根据自己的账户修改

    def init_app(self,app):
        config = app.config
        self.signName = self.SIGN_NAME_FIELD  # 签名
        self.templateCode = self.TEMPLATE_CODE_FIELD  # 模板code
        self.client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, 'cn-hangzhou')
        # try:
        #     self.key = config[self.ACCESS_KEY_ID]
        #     self.secret = config[self.ACCESS_KEY_SECRET]
        #     self.sign_name = config[self.SIGN_NAME_FIELD]
        #     self.code_field = config[self.TEMPLATE_CODE_FIELD]
        # except Exception as e:
        #     logging.error(e.args)
        #     raise ValueError('请填写正确的阿里大鱼配置！')


    def send(self,phone_numbers,code):

        self.signName = self.SIGN_NAME_FIELD  # 签名
        self.templateCode = self.TEMPLATE_CODE_FIELD  # 模板code
        self.client = AcsClient(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET, 'cn-hangzhou')

        self.request = CommonRequest()
        self.request.set_accept_format('json')
        self.request.set_domain('dysmsapi.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_protocol_type('https')
        self.request.set_version('2017-05-25')
        self.request.set_action_name('SendSms')

        self.request.add_query_param('RegionId', "cn-hangzhou")
        self.request.add_query_param('PhoneNumbers', phone_numbers)
        # self.request.add_query_param('SignSource', 3)
        self.request.add_query_param('SignName', self.signName)
        self.request.add_query_param('TemplateCode', self.templateCode)
        self.request.add_query_param('TemplateParam', "{\"code\":\"%s\"}"%code)
        # self.request.add_query_param("Remark", "SMS verification");
        # self.request.add_query_param("SignFileList.1.FileSuffix", "2");
        # self.request.add_query_param("SignFileList.1.FileContents", "3");
        # self.request.add_query_param('RegionId', "cn-hangzhou")
        # self.request.add_query_param('PhoneNumbers', "19801355517")
        # self.request.add_query_param('SignName', "SecondMarket")
        # self.request.add_query_param('TemplateCode', "SMS_190272838")

        response = self.client.do_action_with_exception(self.request)
        return response

#!/usr/bin/env python
#coding=utf-8

# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.request import CommonRequest
# client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
#
# request = CommonRequest()
# request.set_accept_format('json')
# request.set_domain('dysmsapi.aliyuncs.com')
# request.set_method('POST')
# request.set_protocol_type('https') # https | http
# request.set_version('2017-05-25')
# request.set_action_name('SendSms')
#
# request.add_query_param('RegionId', "cn-hangzhou")
# request.add_query_param('PhoneNumbers', "19801355517")
# request.add_query_param('SignName', "Second")
# request.add_query_param('TemplateCode', "111")
#
# response = client.do_action(request)
# # python2:  print(response)
