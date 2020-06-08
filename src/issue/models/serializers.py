from profile.models.profile import Profile

from marshmallow import Schema, ValidationError, fields, validates

from issue.models.issue import Issue
from tag.models.tag import Tag


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
    issue_id = fields.UUID()
    owner = fields.Method('get_owner')
    tags = fields.Method('get_tags')
    title = fields.Str()
    description = fields.Str()
    developer_ids = fields.List(cls_or_instance=fields.UUID)
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def get_owner(self, issue):
        try:
            owner = Profile.get(user_id=issue.owner_id)
        except Profile.DoesNotExist:
            return {}
        else:
            return {'nickname': owner.nickname, 'avatar': owner.avatar}

    def get_tags(self, issue):
        result = []
        checked_tags = list(issue.tags)
        tags = Tag.all()
        for tag in tags:
            try:
                checked_tags.index(tag.name)
            except ValueError:
                checked = False
            else:
                checked = True

            result.append({
                'name': tag.name,
                'description': tag.description,
                'checked': checked
            })

        return sorted(result, key=lambda _tag: _tag['checked'], reverse=True)

    def get_developers(self, issue):
        result = []
        checked_developer_ids = list(issue.developer_ids)
        for developer_id in checked_developer_ids:
            try:
                profile = Profile.get(user_id=developer_id)
            except Profile.DoesNotExist:
                continue

            result.append({
                'user_id': profile.user_id,
                'nickname': profile.nickname
            })
        return result


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


class MultiQueryIssuesSerializer(Schema):
    """反序列化 查询issue的数据
    """
    product_id = fields.UUID(required=True)
    status = fields.Str(required=True)
    limit = fields.Integer(missing=10)
    start = fields.Integer(missing=0)

    @validates('status')
    def validate_status(self, value):
        if value not in [Issue.STATUS_OPENING, Issue.STATUS_CLOSED]:
            raise ValidationError('Only accept "opening" or "closed"')

    @validates('limit')
    def validate_limit(self, value):
        if value < 0 or 20 < value:
            raise ValidationError('Only accept between 0 and 20')

    @validates('start')
    def validate_start(self, value):
        if value < 0:
            raise ValidationError('Only accept greater than 0')


class AssignIssueSerializer(Schema):
    """委派给开发人员
    """
    issue_id = fields.UUID(required=True)
    developer_id = fields.UUID(required=True)


class UpdateIssueTagSerializer(Schema):
    """更新 issue 标签
    """
    issue_id = fields.UUID(required=True)
    tags_name = fields.List(cls_or_instance=fields.Str, required=True)


class DeveloperSerializer(Schema):
    user_id = fields.UUID()
    nickname = fields.Str()


class MultiGetDeveloperSerializer(Schema):
    issue_id = fields.UUID(required=True)
    nickname = fields.Str(missing='')
    limit = fields.Integer(missing=15)
    start = fields.Integer(missing=0)
