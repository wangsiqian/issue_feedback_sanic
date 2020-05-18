from libs.email_utils import EmailUtils
from projector.handler.base_handler import BaseEventHandler


class SendCodeHandler(BaseEventHandler):
    def do_something(self):
        account_id = self.message.get('account_id', '')
        validate_code = self.message.get('validate_code', '')
        if not account_id or not validate_code:
            # 数据验证
            return

        email_utils = EmailUtils()
        # 发送邮件
        email_utils.send(account_id, validate_code)
