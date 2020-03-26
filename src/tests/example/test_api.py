import uuid

from tests.docs import api_docs


def kong_user_header(user_id):
    return {'x-authenticated-userid': str(user_id)}


class TestApi:
    """测试客户端API
    """
    @api_docs(title='示例用 API',
              path='/v1/example',
              method='POST',
              body={'example_field': 'example'},
              file='readme.md')
    async def test_example_api(self, client):
        # Fixme: 添加测试, 更改方法命名

        user_id = str(uuid.uuid4())
        response = await client.post('/v1/example',
                                     headers={
                                         'x-authenticated-userid':
                                         str(user_id),
                                         'App-Id': 'teen_patti_pro'
                                     },
                                     json={'example_field': 'example'})

        assert response.status == 200
        json_result = await response.json()
        print(json_result)
        assert json_result['ok'] is True
        return {'正常响应': json_result}
