import uuid


class CommentService:
    @classmethod
    async def create_comment(cls, client, issue_id, user_id, receiver_id=None):
        url = '/service/v1/comment'
        response = await client.post(url,
                                     json={
                                         'issue_id': issue_id,
                                         'user_id': user_id,
                                         'receiver_id': receiver_id,
                                         'content': '不错的建议'
                                     })

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']


class TestCommentServices(CommentService):
    async def test_create_comment(self, client):
        url = '/service/v1/comment'
        response = await client.post(url,
                                     json={
                                         'issue_id': str(uuid.uuid4()),
                                         'user_id': str(uuid.uuid4()),
                                         'receiver_id': str(uuid.uuid4()),
                                         'content': '不错的建议'
                                     })

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        print(json_result)
        assert json_result['result']['content'] == '不错的建议'

    async def test_list_comments(self, client):
        issue_id = str(uuid.uuid4())
        await self.create_comment(client, issue_id, str(uuid.uuid4()))
        await self.create_comment(client, issue_id, str(uuid.uuid4()))
        await self.create_comment(client, issue_id, str(uuid.uuid4()))
        await self.create_comment(client, issue_id, str(uuid.uuid4()))

        # 另一个返回的评论
        await self.create_comment(client, str(uuid.uuid4()), str(uuid.uuid4()))

        url = f'/service/v1/comments/{issue_id}'
        response = await client.get(url)
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        comments = json_result['result']['comments']
        assert len(comments) == 4
