from datetime import datetime

from cassandra.cqlengine import columns

from libs.aiocqlengine.models import AioModel


class Tag(AioModel):
    """标签
    """
    __table_name__ = 'tag'
    name = columns.Text(primary_key=True)
    description = columns.Text()

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, name, description):
        return await Tag.async_create(name=name, description=description)
