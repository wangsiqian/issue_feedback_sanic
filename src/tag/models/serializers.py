from marshmallow import Schema, fields


class CreateTagSerializer(Schema):
    """反序列化创建标签
    """
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class TagSerializer(Schema):
    """序列化标签
    """
    name = fields.Str(required=True)
    description = fields.Str(required=True)
