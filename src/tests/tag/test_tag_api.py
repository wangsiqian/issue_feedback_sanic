from tests.docs import api_docs


class TagApi:
    async def create_tag(self, client, name, description):
        url = '/service/v1/tag'
        response = await client.post(url,
                                     json={
                                         'name': name,
                                         'description': description
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']


class TestTagService(TagApi):
    @api_docs(title='列出标签', path='/v1/tags', method='GET')
    async def test_list_tags(self, client):
        await self.create_tag(client, 'Bug', 'Bug')
        await self.create_tag(client, 'Help', 'Help')
        await self.create_tag(client, 'Enhancement', 'Enhancement')

        url = '/v1/tags'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        tags = json_result['result']['tags']
        assert len(tags) == 3
        return {'正确响应': json_result}
