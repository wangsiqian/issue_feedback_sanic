import re

from marshmallow import Schema, fields, validates

from account.exceptions import PasswordIllegal


class CreateAccountSerializer(Schema):
    """用于反序列化请求的数据
    """
    account_id = fields.Email(required=True)
    password = fields.Str(required=True)
    role_id = fields.Str(missing='')

    @validates('password')
    def validate_password(self, value):
        """验证密码
        """
        password_regex = re.compile(
            '^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9.~!@&%#_]{8,16}$',
            re.IGNORECASE | re.UNICODE)
        if not password_regex.match(value):
            raise PasswordIllegal


class LoginSerializer(Schema):
    """登陆反序列化
    """
    account_id = fields.Email(required=True)
    password = fields.Str(required=True)


class SessionSerializer(Schema):
    """token 序列化
    """
    token = fields.Str(required=True)
    user_id = fields.UUID(required=True)
    role_id = fields.Str(required=True)
