import uuid
from datetime import datetime

import bcrypt
import ujson
from aio_pika import Message
from cassandra.cqlengine import columns

from app import app
from libs.aiocqlengine.models import AioModel


class Account(AioModel):
    __table_name__ = 'account'

    account_id = columns.Text(primary_key=True)
    user_id = columns.UUID(required=True)
    password = columns.Bytes(required=True)
    salt = columns.Bytes(required=True)

    # 默认没有身份
    role_id = columns.Text(default='')
    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, account_id, role_id, password: str):
        # 生成盐
        salt = bcrypt.gensalt()
        # 密码加密
        encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user_id = str(uuid.uuid4())
        account = await Account.async_create(account_id=account_id,
                                             user_id=user_id,
                                             role_id=role_id,
                                             password=encrypted_password,
                                             salt=salt)

        # 发送创建 profile 的信息
        await app.exchange.publish(
            Message(ujson.dumps({
                'user_id': user_id,
                'event': 'create_profile'
            }).encode(),
                    content_type='application/json'),
            app.config.RABBITMQ_ROUTING_KEY)
        return account
