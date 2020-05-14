from marshmallow import Schema, ValidationError, fields, validates


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


class IssueVoteSerializer(Schema):
    """反序列化对反馈投票的数据
    """
    issue_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    opinion = fields.Str(required=True)

    @validates('opinion')
    def validate_opinion(self, value):
        opinions = ['like', 'dislike']
        if value not in opinions:
            raise ValidationError('Only accept "like" or "dislike".')


class IssueVoteRecordSerializer(Schema):
    """序列化投票记录
    """
    issue_id = fields.UUID()
    user_id = fields.UUID()
    opinion = fields.Str()


class IssueIdSerializer(Schema):
    """反序列化 issue id
    """
    issue_id = fields.UUID(required=True)


class StatisticsSerializer(Schema):
    issue_id = fields.UUID()
    likes = fields.Integer()
    dislikes = fields.Integer()
