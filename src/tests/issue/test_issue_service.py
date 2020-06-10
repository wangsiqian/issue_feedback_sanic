import uuid

from tests.profile.test_profile_service import ProfileService
from tests.tag.test_tag_service import TagService

from app import app


class IssueService:
    @classmethod
    async def create_issue(cls, client, product_id, owner_id, title):
        response = await client.post('/service/v1/issue',
                                     json={
                                         'product_id': product_id,
                                         'owner_id': owner_id,
                                         'title': title
                                     })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']['issue_id']

    async def get_issue_by_id(self, client, issue_id):
        response = await client.get(f'/service/v1/issue/{issue_id}')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']


class TestIssueService(IssueService, TagService, ProfileService):
    async def test_create_issue(self, client):
        url = '/service/v1/issue'

        product_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())
        response = await client.post(url,
                                     json={
                                         'product_id': product_id,
                                         'owner_id': owner_id,
                                         'title': '反馈标题'
                                     })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        issue = json_result['result']
        assert issue['title'] == '反馈标题'
        assert issue['status'] == 'opening'
        assert issue['description'] == ''

    async def test_user_vote_for_issue(self, client):
        user_id = str(uuid.uuid4())
        issue_id = await self.create_issue(client=client,
                                           product_id=str(uuid.uuid4()),
                                           owner_id=user_id,
                                           title='反馈')

        url = f'/service/v1/issue/{issue_id}/vote'
        # 投票
        response = await client.put(url,
                                    json={
                                        'opinion': 'like',
                                        'user_id': user_id
                                    })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        record = json_result['result']
        assert record['issue_id'] == issue_id
        assert record['user_id'] == user_id
        assert record['opinion'] == 'like'

        # 获取统计数据
        response2 = await client.get(f'/service/v1/issue/{issue_id}/statistics'
                                     )
        assert response2.status == 200

        json_result2 = await response2.json()
        assert json_result2['result']['issue_id'] == issue_id
        assert json_result2['result']['likes'] == 1
        assert json_result2['result']['dislikes'] == 0

        # 二次投票
        await client.put(url, json={'opinion': 'dislike', 'user_id': user_id})

        response3 = await client.get(f'/service/v1/issue/{issue_id}/statistics'
                                     )
        assert response3.status == 200

        json_result3 = await response3.json()
        assert json_result3['result']['issue_id'] == issue_id
        # 变为 0
        assert json_result3['result']['likes'] == 0
        assert json_result3['result']['dislikes'] == 1

    async def test_update_issue(self, client):
        product_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())
        # 创建两个反馈
        issue_id = await self.create_issue(client=client,
                                           product_id=product_id,
                                           owner_id=owner_id,
                                           title='反馈1')

        # 更新
        url = f'/service/v1/issue/{issue_id}'
        await client.put(url,
                         json={
                             'owner_id': owner_id,
                             'title': 'new',
                             'description': 'new'
                         })

        issue = await self.get_issue_by_id(client, issue_id)
        assert issue['title'] == 'new'
        assert issue['description'] == 'new'

    async def test_list_issues_by_product_id(self, client):
        product_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())
        # 创建两个反馈
        await self.create_issue(client=client,
                                product_id=product_id,
                                owner_id=owner_id,
                                title='反馈1')
        await self.create_issue(client=client,
                                product_id=product_id,
                                owner_id=owner_id,
                                title='反馈2')

        # 另一个产品的反馈
        await self.create_issue(client=client,
                                product_id=str(uuid.uuid4()),
                                owner_id=owner_id,
                                title='反馈2')

        response = await client.get(
            f'/service/v1/issue/product/{product_id}?status=opening')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        issues = json_result['result']['issues']
        print(issues)
        # 返回两个反馈
        assert len(issues) == 2
        assert json_result['result']['count'] == 2

        # 测试分页
        response2 = await client.get(
            f'/service/v1/issue/product/{product_id}?status=opening&limit=1&start=0'
        )
        assert response2.status == 200

        json_result2 = await response2.json()
        assert json_result2['ok']

        filtered_issues = json_result2['result']['issues']
        # 返回一个反馈
        assert len(filtered_issues) == 1
        print(filtered_issues)
        assert json_result2['result']['count'] == 2

    async def test_update_issue_tags(self, client):
        # 创建标签
        await self.create_tag(client, 'Bug', 'Bug', '#eb4034')
        await self.create_tag(client, 'Help', 'Help', '#eb4034')
        await self.create_tag(client, 'Enhancement', 'Enhancement', '#eb4034')

        issue_id = await self.create_issue(client,
                                           product_id=str(uuid.uuid4()),
                                           owner_id=str(uuid.uuid4()),
                                           title='产品有 bug')
        url = f'/service/v1/issue/{issue_id}/tag'
        response = await client.put(url, json={'tags_name': ['Bug', 'Help']})
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        # 查询 issue
        issue = await self.get_issue_by_id(client, issue_id)
        tags = issue['tags']
        assert len(tags) == 3
        assert tags[0]['name'] == 'Bug'
        assert tags[0]['checked'] is True
        assert tags[1]['name'] == 'Help'
        assert tags[1]['checked'] is True
        assert tags[2]['name'] == 'Enhancement'
        assert tags[2]['checked'] is False

        # 再次更新
        await client.put(url,
                         json={'tags_name': ['Bug', 'Help', 'Enhancement']})

        issue = await self.get_issue_by_id(client, issue_id)
        tags = issue['tags']
        assert tags[0]['name'] == 'Enhancement'
        assert tags[0]['checked'] is True
        assert tags[1]['name'] == 'Bug'
        assert tags[1]['checked'] is False
        assert tags[2]['name'] == 'Help'
        assert tags[2]['checked'] is False

    async def test_list_developers(self, client):
        await self.create_profile(client, str(uuid.uuid4()), 'tester1',
                                  app.config.ROLE_DEVELOPER)
        await self.create_profile(client, str(uuid.uuid4()), 'tester2',
                                  app.config.ROLE_DEVELOPER)
        await self.create_profile(client, str(uuid.uuid4()), 'tester3',
                                  app.config.ROLE_DEVELOPER)
        await self.create_profile(client, str(uuid.uuid4()), 'tester4',
                                  app.config.ROLE_DEVELOPER)

        issue_id = await self.create_issue(client, str(uuid.uuid4()),
                                           str(uuid.uuid4()), '有问题')
        url = f'/service/v1/issue/{issue_id}/developers'
        response1 = await client.get(url)
        assert response1.status == 200

        json_result2 = await response1.json()
        assert json_result2['ok']
        developers = json_result2['result']['developers']
        assert len(developers) == 4

        response2 = await client.get(f'{url}?nickname=ter1')
        assert response2.status == 200

        json_result2 = await response2.json()
        assert json_result2['ok']
        developers = json_result2['result']['developers']
        assert len(developers) == 1

    async def test_modify_issue_status(self, client):
        owner_id = str(uuid.uuid4())
        issue_id = await self.create_issue(client=client,
                                           product_id=str(uuid.uuid4()),
                                           owner_id=owner_id,
                                           title='反馈1')
        issue = await self.get_issue_by_id(client, issue_id)
        assert issue['status'] == 'opening'

        url = f'/service/v1/issue/{issue_id}/status'
        # 修改状态
        await client.put(url, json={'user_id': owner_id, 'status': 'closed'})
        issue = await self.get_issue_by_id(client, issue_id)
        assert issue['status'] == 'closed'

        # 非创建人来关闭
        error_response = await client.put(url,
                                          json={
                                              'user_id': str(uuid.uuid4()),
                                              'status': 'opening'
                                          })
        assert error_response.status == 200
        error_result = await error_response.json()
        assert error_result['error_type'] == 'permission_denied'
        assert error_result['message'] == '没有权限'
