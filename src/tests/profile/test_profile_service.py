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
