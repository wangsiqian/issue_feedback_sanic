import uuid


class TestProfileService:
    async def test_create_profile(self, client):
        url = '/service/v1/profile'

        user_id = str(uuid.uuid4())
        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                     })

        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        assert json_result['result']['user_id'] == user_id
        assert json_result['result']['nickname'] == 'tester'
        assert json_result['result']['gender'] == 1

    async def test_get_profile(self, client):
        user_id = str(uuid.uuid4())
        # 创建 profile
        await client.post('/service/v1/profile',
                          json={
                              'user_id': user_id,
                              'nickname': 'tester',
                              'gender': 0
                          })

        response = await client.get(f'/service/v1/profile/{user_id}')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        profile = json_result['result']
        assert profile['user_id'] == user_id
        assert profile['nickname'] == 'tester'
        assert profile['gender'] == 0
        assert profile['avatar'] == ''
