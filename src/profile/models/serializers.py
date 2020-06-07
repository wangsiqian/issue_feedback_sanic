from marshmallow import Schema, fields, validates, ValidationError

from app import app


class CreateProfileSerializer(Schema):
    """用于反序列化创建 profile 的数据
    """
    user_id = fields.UUID(required=True)
    nickname = fields.Str(required=True)
    gender = fields.Integer(missing=1)
    role_id = fields.Str(missing=app.config.ROLE_USER)

    @validates('role_id')
    def validate_role_id(self, value):
        if value not in app.config.ROLES:
            raise ValidationError('有内鬼，中止交易！')


class UpdateProfileSerializer(Schema):
    """用于反序列化创建 profile 的数据
    """
    user_id = fields.UUID(required=True)
    nickname = fields.Str()
    gender = fields.Integer()


class ProfileSerializer(Schema):
    """序列化 profile
    """
    user_id = fields.UUID()
    gender = fields.Integer()
    nickname = fields.Str()
    avatar = fields.Str()
    role_id = fields.Str()


class UserIdSerializer(Schema):
    """反序列化 user_id
    """
    user_id = fields.UUID(required=True)
