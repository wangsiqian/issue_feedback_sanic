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

    issue_id = columns.UUID(primary_key=True)
    owner_id = columns.UUID()
    title = columns.Text()
    description = columns.Text()

    tags = columns.List(value_type=columns.Text)
    developer_ids = columns.List(value_type=columns.UUID)
    # 默认开放
    status = columns.Text(default=STATUS_OPENING, index=True)

    created_at = columns.DateTime(default=datetime.utcnow)
    updated_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, product_id, owner_id, title, description):
        issue_id = str(uuid.uuid4())
        issue = await Issue.async_create(issue_id=issue_id,
                                         owner_id=owner_id,
                                         title=title,
                                         description=description)

        # 分区
        await IssueByProduct.new(product_id, issue_id)
        await IssueByUser.new(owner_id, issue_id)

        return issue

    async def close_issue(self):
        self.status = self.STATUS_CLOSED
        await self.async_save()

    async def open_issue(self):
        self.status = self.STATUS_OPENING
        await self.async_save()

    async def handle_developer(self, developer_id):
        developer_ids = list(self.developer_ids)
        try:
            developer_ids.remove(developer_id)
        except ValueError:
            # 如果不存在则添加
            developer_ids.append(developer_id)

        self.developer_ids = developer_ids

    async def handle_tags(self, tags_name):
        tags = list(self.tags)
        for tag_name in tags_name:
            # 批量添加或删除标签
            try:
                tags.remove(tag_name)
            except ValueError:
                tags.append(tag_name)

        self.tags = tags
        await self.async_save()


class IssueByProduct(AioModel):
    """按产品分区
    """
    __table_name__ = 'issue_by_product'

    product_id = columns.UUID(partition_key=True)
    issue_id = columns.UUID(primary_key=True)
    created_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, product_id, issue_id):
        await IssueByProduct.async_create(product_id=product_id,
                                          issue_id=issue_id)


class IssueByUser(AioModel):
    """按创建者分区
    """
    __table_name__ = 'issue_by_user'

    owner_id = columns.UUID(partition_key=True)
    issue_id = columns.UUID(primary_key=True)
    created_at = columns.DateTime(default=datetime.utcnow)

    @classmethod
    async def new(cls, owner_id, issue_id):
        await IssueByUser.async_create(owner_id=owner_id, issue_id=issue_id)


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
        new_statistics = {}
        # 更改看法
        old_field = cls.OPINION_TO_FIELD.get(old_opinion)
        if old_field:
            new_statistics.update({old_field: -1})

        new_field = cls.OPINION_TO_FIELD.get(new_opinion)
        if new_field:
            new_statistics.update({new_field: 1})

        if new_statistics:
            await IssueVoteStatistics(issue_id=issue_id
                                      ).async_update(**new_statistics)
