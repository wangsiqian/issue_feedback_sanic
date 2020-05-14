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
        assert issue['product_id'] == product_id
        assert issue['owner_id'] == owner_id
        assert issue['title'] == '反馈标题'
        assert issue['status'] == 'opening'
        assert issue['description'] == ''

        # 再次创建
        error_response1 = await client.post(url,
                                            json={
                                                'product_id': product_id,
                                                'owner_id': owner_id,
                                                'title': '反馈标题'
                                            })
        assert error_response1.status == 200

        error_result1 = await error_response1.json()
        assert error_result1['error_type'] == 'issue_already_exist'
        assert error_result1['message'] == '您已经反馈过相关问题了'

    async def test_user_vote_for_issue(self, client):
        user_id = str(uuid.uuid4())
        issue_id = await IssueService.create_issue(client=client,
                                                   product_id=str(
                                                       uuid.uuid4()),
                                                   owner_id=user_id,
                                                   title='反馈')

        url = f'/service/v1/issue/{issue_id}/user/{user_id}/vote'
        # 投票
        response = await client.put(url, json={'opinion': 'like'})
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
        await client.put(url, json={'opinion': 'dislike'})

        response3 = await client.get(f'/service/v1/issue/{issue_id}/statistics'
                                     )
        assert response3.status == 200

        json_result3 = await response3.json()
        assert json_result3['result']['issue_id'] == issue_id
        # 变为 0
        assert json_result3['result']['likes'] == 0
        assert json_result3['result']['dislikes'] == 1
