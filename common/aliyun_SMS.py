import json
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions


class AliyunMessage:
    def __init__(self):
        self.endpoint = 'dysmsapi.aliyuncs.com'
        # AccessKey ID,
        self.access_key_id = 'LTAI5t9gzCNq64cdiGn1VpF2'
        # AccessKey Secret,
        self.access_key_secret = 'QG8F5CSmXBR19zYbEWIyPtTar5De9f'
        # 申请的签名
        self.sign_name = '阿里云短信测试'
        # 短信模板
        self.template_code = 'SMS_154950909'

    def send_msg(self, mobile: str, code: str):
        """
        :param mobile: 接受验证码的手机号
        :param code: 验证码内容
        :return:
        """
        message = SendSmsRequest(
            sign_name=self.sign_name,
            template_code=self.template_code,
            phone_numbers=mobile,
            template_param=json.dumps({"code": code})
        )
        config = Config(access_key_id=self.access_key_id,
                        access_key_secret=self.access_key_secret,
                        endpoint=self.endpoint)
        client = Client(config)
        runtime = RuntimeOptions()
        try:
            # 发送短信
            res = client.send_sms_with_options(message, runtime)
            if res.body.code == 'OK':
                return {'code': "OK", "message": "短信发送成功"}
            else:
                return {'code': "NO", "error": res.body.message}
        except Exception as e:
            return {'code': "NO", "error": '短信发送失败'}


if __name__ == '__main__':
    AliyunMessage().send_msg('19925331148', '989829')