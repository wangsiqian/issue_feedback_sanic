from marshmallow import Schema, fields


class OwnerIdSerializer(Schema):
    """用于反序列化owner_id
    """
    owner_id = fields.UUID(required=True)


class UserCounterSerializer(Schema):
    """序列化用户统计数据
    """
    total_count = fields.Integer()
    solved_count = fields.Integer()
