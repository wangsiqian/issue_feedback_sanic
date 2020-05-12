import uuid

from marshmallow import Schema, fields


class CreateProfileSerializer(Schema):
    """用于反序列化创建 profile 的数据
    """
    user_id = fields.UUID(missing=str(uuid.uuid4()))
    nickname = fields.Str(required=True)
    gender = fields.Integer(missing=1)


class ProfileSerializer(Schema):
    """序列化 profile
    """
    user_id = fields.UUID()
    gender = fields.Integer()
    nickname = fields.Str()
    avatar = fields.Str()


class UserIdSerializer(Schema):
    """反序列化 user_id
    """
    user_id = fields.UUID(required=True)
