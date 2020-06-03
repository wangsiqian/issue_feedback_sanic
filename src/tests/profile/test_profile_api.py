import uuid
from tests.docs import api_docs


class ProfileApi:
    @classmethod
    async def create_profile(cls, client, user_id):
        url = '/v1/profile'
        await client.post(url,
                          json={
                              'user_id': user_id,
                              'nickname': 'tester',
                          })


class TestProfileApi:
    @api_docs(title='创建个人资料',
              path='v1/profile',
              method='POST',
              body={
                  'user_id(必填)': '用户id',
                  'nickname(必填)': '用户昵称',
                  'gender': '性别'
              })
    async def test_create_profile(self, client):
        url = '/v1/profile'

        user_id = str(uuid.uuid4())
        response = await client.post(url,
                                     json={
                                         'user_id': user_id,
                                         'nickname': 'tester',
                                     })

        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']
        return {'正确响应': json_result}

    @api_docs(title='获取个人资料', path='/v1/profile/{user_id}', method='GET')
    async def test_get_profile(self, client):
        user_id = str(uuid.uuid4())
        # 创建 profile
        await client.post('/service/v1/profile',
                          json={
                              'user_id': user_id,
                              'nickname': 'tester',
                              'gender': 0
                          })

        response = await client.get(f'/v1/profile/{user_id}')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        profile = json_result['result']
        assert profile['user_id'] == user_id
        assert profile['nickname'] == 'tester'
        assert profile['gender'] == 0
        assert profile['avatar'] == ''
        return {'正确响应': json_result}

    @api_docs(title='更新个人资料',
              path='/v1/profile/{user_id}',
              method='PUT',
              body={
                  'nickname': '昵称',
                  'gender': '性别'
              })
    async def test_update_profile(self, client):
        user_id = str(uuid.uuid4())
        # 创建 profile
        await client.post('/service/v1/profile',
                          json={
                              'user_id': user_id,
                              'nickname': 'tester',
                              'gender': 1
                          })

        # 查询
        response = await client.get(f'/service/v1/profile/{user_id}')
        assert response.status == 200
        json_result = await response.json()

        profile = json_result['result']
        assert profile['nickname'] == 'tester'
        assert profile['gender'] == 1

        # 更新 profile
        response3 = await client.put(f'/v1/profile/{user_id}',
                                     json={
                                         'nickname': 'tester2',
                                         'gender': 0
                                     })
        assert response3.status == 200
        json_result1 = await response3.json()
        # 再次查询
        response2 = await client.get(f'/service/v1/profile/{user_id}')
        assert response2.status == 200
        json_result2 = await response2.json()

        new_profile = json_result2['result']
        assert new_profile['nickname'] == 'tester2'
        assert new_profile['gender'] == 0
        return {'正确响应': json_result1}
