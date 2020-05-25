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
    status = columns.Text(default=STATUS_OPENING, index=True)
    issue_id = columns.UUID(default=str(uuid.uuid4()))

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, product_id, owner_id, title, description):
        return await Issue.async_create(product_id=product_id,
                                        owner_id=owner_id,
                                        title=title,
                                        description=description)


class IssueVoteRecord(AioModel):
    """投票记录表
    """
    __table_name__ = 'issue_vote_record'

    issue_id = columns.UUID(partition_key=True)
    user_id = columns.UUID(primary_key=True)

    OPINION_NONE = 'none'
    OPINION_LIKE = 'like'
    OPINION_DISLIKE = 'dislike'
    opinion = columns.Text(default=OPINION_NONE)

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new_record(cls, issue_id, user_id, opinion):
        vote = await IssueVoteRecord.async_create(issue_id=issue_id,
                                                  user_id=user_id,
                                                  opinion=opinion)

        await IssueVoteStatistics.update_statistics(
            issue_id=issue_id,
            opinion=opinion,
            action=IssueVoteStatistics.ACTION_INCREMENT)

        return vote

    async def update_record(self, issue_id, opinion):
        if self.opinion == opinion:
            # 再次点击相等的选项则消除
            await IssueVoteStatistics.update_statistics(
                issue_id=issue_id,
                opinion=opinion,
                action=IssueVoteStatistics.ACTION_DECREMENT)

            # 设置为 none
            self.opinion = self.OPINION_NONE
        else:
            # 更换
            await IssueVoteStatistics.change_opinion(issue_id=issue_id,
                                                     old_opinion=self.opinion,
                                                     new_opinion=opinion)
            self.opinion = opinion

        await self.async_save()


class IssueVoteStatistics(AioModel):
    """反馈统计数据
    """
    __table_name__ = 'issue_vote_statistics'

    issue_id = columns.UUID(primary_key=True)
    likes = columns.Counter()
    dislikes = columns.Counter()

    OPINION_TO_FIELD = {'like': 'likes', 'dislike': 'dislikes'}
    ACTION_INCREMENT = 1
    ACTION_DECREMENT = -1

    @classmethod
    async def update_statistics(cls, issue_id, opinion, action):
        # 获取需要更新的字段
        field = IssueVoteStatistics.OPINION_TO_FIELD.get(opinion)
        if field:
            await IssueVoteStatistics(issue_id=issue_id
                                      ).async_update(**{field: action})

    @classmethod
    async def change_opinion(cls, issue_id, old_opinion, new_opinion):
        # 更改看法
        old_field = cls.OPINION_TO_FIELD.get(old_opinion)
        new_field = cls.OPINION_TO_FIELD.get(new_opinion)
        if old_field and new_field:
            await IssueVoteStatistics(issue_id=issue_id
                                      ).async_update(**{
                                          old_field: -1,
                                          new_field: 1
                                      })
