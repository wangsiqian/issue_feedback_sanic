class TagService:
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


class TestTagService(TagService):
    async def test_create_tag(self, client):
        url = '/service/v1/tag'
        response = await client.post(url,
                                     json={
                                         'name': 'Bug',
                                         'description': '程序运行异常'
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        assert json_result['result']['name'] == 'Bug'
        assert json_result['result']['description'] == '程序运行异常'

    async def test_list_tags(self, client):
        await self.create_tag(client, 'Bug', 'Bug')
        await self.create_tag(client, 'Help', 'Help')
        await self.create_tag(client, 'Enhancement', 'Enhancement')

        url = '/service/v1/tags'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        tags = json_result['result']['tags']
        assert len(tags) == 3
