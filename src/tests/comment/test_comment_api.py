import uuid

from tests.docs import api_docs
from tests.account.test_account_service import AccountService

from app import app


class CommentApi:
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


class TestCommentApi(CommentApi):
    @api_docs(title='创建评论',
              path='/v1/comment',
              method='POST',
              body={
                  'issue_id(必填)': '问题id',
                  'user_id(必填)': '用户id',
                  'receiver_id(必填)': '接收者id',
                  'content(必填)': '内容'
              },
              headers={'Authorization': '用户 Token'})
    async def test_create_comment(self, client):
        url = '/v1/comment'
        token = await AccountService.get_token(client, app.config.ROLE_USER)
        response = await client.post(url,
                                     json={
                                         'issue_id': str(uuid.uuid4()),
                                         'user_id': str(uuid.uuid4()),
                                         'receiver_id': str(uuid.uuid4()),
                                         'content': '不错的建议'
                                     },
                                     headers={'Authorization': token})

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return {'正确响应': json_result}

    @api_docs(title='获取评论列表', path='/v1/comments/{issue_id}', method='GET')
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

        return {'正确响应': json_result}
