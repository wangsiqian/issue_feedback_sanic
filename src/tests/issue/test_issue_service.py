import uuid


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
