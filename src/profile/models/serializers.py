import uuid

from marshmallow import Schema, fields


class ProfileSerializer(Schema):
    """用于反序列化请求的数据
    """
    user_id = fields.UUID(missing=str(uuid.uuid4()))
    nickname = fields.Str(required=True)
    gender = fields.Integer(missing=1)
