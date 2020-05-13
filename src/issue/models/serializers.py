from marshmallow import Schema, fields


class CreateIssueSerializer(Schema):
    """用于反序列化创建 issue 的数据
    """
    product_id = fields.UUID(required=True)
    owner_id = fields.UUID(required=True)
    title = fields.Str(required=True)
    description = fields.Str(missing='')


class IssueSerializer(Schema):
    """序列化反馈返回的数据
    """
    product_id = fields.UUID()
    owner_id = fields.UUID()
    issue_id = fields.UUID()
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
