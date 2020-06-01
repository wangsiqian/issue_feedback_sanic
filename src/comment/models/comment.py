import uuid
from datetime import datetime

from cassandra.cqlengine import columns

from libs.aiocqlengine.models import AioModel


class Comment(AioModel):
    """评论
    """
    __table_name__ = 'comment'
    comment_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(required=True)
    issue_id = columns.UUID(required=True, index=True)
    receiver_id = columns.UUID()
    content = columns.Text()
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, user_id, issue_id, content, receiver_id=None):
        return await Comment.async_create(comment_id=str(uuid.uuid4()),
                                          user_id=user_id,
                                          issue_id=issue_id,
                                          content=content,
                                          receiver_id=receiver_id)
