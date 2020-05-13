import uuid
from datetime import datetime

from cassandra.cqlengine import columns

from libs.aiocqlengine.models import AioModel


class Issue(AioModel):
    """需求、反馈
    """
    __table_name__ = 'issue'

    STATUS_OPENING = 'opening'
    STATUS_CLOSED = 'closed'

    product_id = columns.UUID(partition_key=True)
    owner_id = columns.UUID(primary_key=True)
    title = columns.Text(primary_key=True)
    description = columns.Text()

    # 默认开放
    status = columns.Text(default=STATUS_OPENING)
    issue_id = columns.UUID(default=str(uuid.uuid4()))

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, product_id, owner_id, title, description):
        return await Issue.async_create(product_id=product_id,
                                        owner_id=owner_id,
                                        title=title,
                                        description=description)
