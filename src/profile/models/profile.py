from datetime import datetime

from cassandra.cqlengine import columns

from libs.aiocqlengine.models import AioModel


class Profile(AioModel):
    __table_name__ = 'profile'

    user_id = columns.UUID(primary_key=True)
    nickname = columns.Text()
    avatar = columns.Text(default='')
    gender = columns.TinyInt(default=1)

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, user_id, nickname, gender):
        return await Profile.async_create(user_id=user_id,
                                          nickname=nickname,
                                          gender=gender)

    async def update_profile(self, **profiles):
        profiles['updated_at'] = datetime.utcnow()
        new_profile = await self.async_update(**profiles)
        return new_profile
