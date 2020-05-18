import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException

from configs.loader import load_config

config = load_config()
logger = logging.getLogger('email_utils')


class EmailUtils(object):
    message_template = '【软件反馈收集系统】您的验证码是{code}，在3分钟内有效。如非本人操作请忽略本邮件。'

    def __init__(self):
        self.email_address = config.EMAIL_ADDRESS
        self.email_password = config.EMAIL_PASSWORD

        self.mime_multipart = MIMEMultipart()
        self.server = SMTP_SSL('smtp.qq.com', 465)

    def send(self, email, code):
        """发送email
        """
        if not self.email_address or not self.email_password:
            return
        self.server.login(self.email_address, self.email_password)

        mime_multipart = MIMEMultipart()
        mime_multipart['From'] = '@软件反馈收集系统'
        mime_multipart['Subject'] = '验证码'
        mime_multipart.attach(
            MIMEText(self.message_template.format(code=code), 'plain',
                     'utf-8'))
        try:
            self.server.sendmail(email, [email], mime_multipart.as_string())
        except SMTPException as error:
            logger.error(error)
        self.server.close()
