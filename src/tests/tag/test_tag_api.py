from tests.docs import api_docs
from tests.tag.test_tag_service import TagService


class TestTagService(TagService):
    @api_docs(title='列出标签', path='/v1/tags', method='GET')
    async def test_list_tags(self, client):
        await self.create_tag(client, 'Bug', 'Bug', '#eb4034')
        await self.create_tag(client, 'Help', 'Help', '#eb4034')
        await self.create_tag(client, 'Enhancement', 'Enhancement', '#eb4034')

        url = '/v1/tags'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        tags = json_result['result']['tags']
        assert len(tags) == 3
        return {'正确响应': json_result}
