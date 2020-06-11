from profile.models.profile import Profile

from marshmallow import Schema, fields


class CreateCommentSerializer(Schema):
    """反序列化创建留言
    """
    issue_id = fields.UUID(required=True)
    user_id = fields.UUID(required=True)
    receiver_id = fields.UUID(missing=None)
    content = fields.Str(required=True)


class CommentIdSerializer(Schema):
    comment_id = fields.UUID()


class CommentSerializer(Schema):
    """序列化留言
    """
    issue_id = fields.UUID()
    user_id = fields.UUID()
    receiver_id = fields.UUID()
    content = fields.Str()
    created_at = fields.DateTime()


class ListCommentsSerializer(Schema):
    """序列化留言列表
    """
    comment_id = fields.UUID()
    owner = fields.Method('get_owner')
    content = fields.Str()
    created_at = fields.DateTime()

    def get_owner(self, comment):
        try:
            profile = Profile.get(user_id=comment.user_id)
        except Profile.DoesNotExist:
            return {}
        else:
            return {
                'user_id': str(comment.user_id),
                'nickname': profile.nickname,
                'avatar': profile.avatar
            }
