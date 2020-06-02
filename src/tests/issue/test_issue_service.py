import uuid


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


class TestIssueService:
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
        issue_id = await IssueService.create_issue(client=client,
                                                   product_id=str(
                                                       uuid.uuid4()),
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

    async def test_list_issues_by_product_id(self, client):
        product_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())
        # 创建两个反馈
        await IssueService.create_issue(client=client,
                                        product_id=product_id,
                                        owner_id=owner_id,
                                        title='反馈1')
        await IssueService.create_issue(client=client,
                                        product_id=product_id,
                                        owner_id=owner_id,
                                        title='反馈2')

        # 另一个产品的反馈
        await IssueService.create_issue(client=client,
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

    async def test_assign_issue_to_developer(self, client):
        owner_id = str(uuid.uuid4())
        issue_id = await IssueService.create_issue(client=client,
                                                   product_id=str(
                                                       uuid.uuid4()),
                                                   owner_id=owner_id,
                                                   title='反馈1')

        # 分配给开发者
        url = f'/service/v1/issue/{issue_id}/assign'
        developer_id = 'c288acad-37c3-4b36-bf61-aada41fe1b8f'
        response1 = await client.put(url, json={'developer_id': developer_id})
        assert response1.status == 200

        json_result1 = await response1.json()
        assert json_result1['ok']

        issue = json_result1['result']
        assert len(issue['developer_ids']) == 1
        assert issue['developer_ids'][0] == developer_id

        # 再次分配
        response2 = await client.put(url, json={'developer_id': developer_id})
        assert response2.status == 200

        json_result2 = await response2.json()
        assert json_result2['ok']

        issue = json_result2['result']
        assert len(issue['developer_ids']) == 0
