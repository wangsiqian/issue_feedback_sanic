import uuid
from datetime import datetime

from cassandra.cqlengine import columns

from libs.aiocqlengine.models import AioModel


class Product(AioModel):
    """产品信息
    """
    __table_name__ = 'product'

    manager_id = columns.UUID(partition_key=True)
    product_id = columns.UUID(primary_key=True)
    name = columns.Text()
    description = columns.Text()

    created_at = columns.DateTime(default=datetime.utcnow, index=True)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, manager_id, name, description):
        return await Product.async_create(manager_id=manager_id,
                                          product_id=str(uuid.uuid4()),
                                          name=name,
                                          description=description)

    async def update_product(self, **new_product):
        # 清理不需要更新的字段
        new_product.pop('manager_id', '')
        new_product.pop('product_id', '')

        new_product['updated_at'] = datetime.utcnow()
        return await self.async_update(**new_product)
