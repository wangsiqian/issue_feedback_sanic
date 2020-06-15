from marshmallow import Schema, fields


class OwnerIdSerializer(Schema):
    """用于反序列化owner_id
    """
    owner_id = fields.UUID(required=True)


class DeveloperIdSerializer(Schema):
    """用于反序列化 developer_id
    """
    developer_id = fields.UUID(required=True)


class UserCounterSerializer(Schema):
    """序列化用户统计数据
    """
    total_count = fields.Integer()
    solved_count = fields.Integer()


class DeveloperCounterSerializer(Schema):
    """序列化开发人员统计数据
    """
    opening_count = fields.Integer()
    closed_count = fields.Integer()


class ManagerIdSerializer(Schema):
    """用于反序列化 manager_id
    """
    manager_id = fields.UUID(required=True)


class ManagerCounterSerializer(Schema):
    """序列化管理人员统计数据
    """
    total_count = fields.Integer()
    accepted_count = fields.Integer()
    closed_count = fields.Integer()
