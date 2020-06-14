import uuid

from tests.issue.test_issue_service import IssueService


class TestStatisticsService(IssueService):
    async def test_count_issue_by_user(self, client):
        owner_id = str(uuid.uuid4())
        # 创建两个需求
        issue_id = await self.create_issue(client, str(uuid.uuid4()), owner_id,
                                           '测试有问题')
        await self.create_issue(client, str(uuid.uuid4()), owner_id, '这个产品不好')
        await self.create_issue(client, str(uuid.uuid4()), owner_id, '这个产品不错')

        # 关闭一个需求
        url = f'/service/v1/issue/{issue_id}/status'
        await client.put(url, json={'user_id': owner_id, 'status': 'closed'})

        # 获取用户的统计数据
        url = f'/service/v1/statistics/user/{owner_id}'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        assert json_result['result']['total_count'] == 3
        assert json_result['result']['solved_count'] == 1
