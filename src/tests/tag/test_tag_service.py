class TagService:
    async def create_tag(self, client, name, description, color):
        url = '/service/v1/tag'
        response = await client.post(url,
                                     json={
                                         'name': name,
                                         'description': description,
                                         'color': color
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
                                         'description': '程序运行异常',
                                         'color': '#eb4034'
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        assert json_result['result']['name'] == 'Bug'
        assert json_result['result']['description'] == '程序运行异常'
        assert json_result['result']['color'] == '#eb4034'

    async def test_list_tags(self, client):
        await self.create_tag(client, 'Bug', 'Bug', '#eb4034')
        await self.create_tag(client, 'Help', 'Help', '#eb4034')
        await self.create_tag(client, 'Enhancement', 'Enhancement', '#eb4034')

        url = '/service/v1/tags'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        tags = json_result['result']['tags']
        assert len(tags) == 3

    async def test_create_multi_tags(self, client):
        response = await client.post('/service/v1/tags',
                                     json={
                                         'tags': [{
                                             'name': 'Bug',
                                             'description': '程序运行异常',
                                             'color': '#eb4034'
                                         }, {
                                             'name': 'duplicate',
                                             'description': '存在类似的反馈',
                                             'color': '#eb4034'
                                         }]
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        # 获取 tags
        url = '/service/v1/tags'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        tags = json_result['result']['tags']
        assert len(tags) == 2
