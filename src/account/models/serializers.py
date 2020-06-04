import re

from marshmallow import Schema, ValidationError, fields, validates

from account.exceptions import PasswordIllegal
from app import app

config = app.config


class CreateAccountApiSerializer(Schema):
    """用于反序列化API创建账号请求的数据
    """
    account_id = fields.Email(required=True)
    password = fields.Str(required=True)
    validate_token = fields.Str(required=True)
    validate_code = fields.Str(required=True)

    @validates('password')
    def validate_password(self, value):
        """验证密码
        """
        password_regex = re.compile(
            '^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9.~!@&%#_]{8,16}$',
            re.IGNORECASE | re.UNICODE)
        if not password_regex.match(value):
            raise PasswordIllegal


class CreateAccountServiceSerializer(CreateAccountApiSerializer):
    """用于反序列化内部服务创建账号请求的数据
    """
    role_id = fields.Str(missing=config.ROLE_USER)

    @validates('role_id')
    def validate_role_id(self, value):
        if value not in config.ROLES:
            raise ValidationError('有内鬼，中止交易！')


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


class AccountIdSerializer(Schema):
    """反序列化账号ID
    """
    account_id = fields.Email(required=True)


class ValidationSerializer(Schema):
    """序列化邮箱验证生成的 token 数据
    """
    validate_token = fields.Str()
    validate_code = fields.Str()


class ValidationTokenSerializer(Schema):
    """序列化邮箱验证生成的 token 数据
    """
    validate_token = fields.Str()


class UserIdSerializer(Schema):
    """反序列化用户ID
    """
    user_id = fields.UUID(required=True)


class RoleIdSerializer(Schema):
    """获取身份
    """
    role_id = fields.Str()
