from marshmallow import Schema, fields


class CreateProductSerializer(Schema):
    """用于反序列化创建 product 的数据
    """
    manager_id = fields.UUID(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)


class ProductSerializer(Schema):
    """序列化产品返回的数据
    """
    manager_id = fields.UUID()
    product_id = fields.UUID()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()


class ManagerIdSerializer(Schema):
    """反序列化产品ID
    """
    manager_id = fields.UUID(required=True)
