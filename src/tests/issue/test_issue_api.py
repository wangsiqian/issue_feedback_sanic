import uuid

from tests.account.test_account_service import AccountService
from tests.docs import api_docs

from app import app


class TestIssueApi:
    @api_docs(title='用户添加反馈、需求',
              path='/v1/issue',
              method='POST',
              body={
                  'product_id（必填）': '产品ID',
                  'owner_id（必填）': '创建者ID',
                  'title（必填）': '反馈标题',
                  'description（非必填）': '反馈描述'
              },
              headers={'Authentication': '用户 Token'})
    async def test_create_issue(self, client):
        url = '/v1/issue'

        product_id = str(uuid.uuid4())
        owner_id = str(uuid.uuid4())

        # 获取用户身份的token
        token = await AccountService.get_token(client, app.config.ROLE_USER)
        response = await client.post(url,
                                     json={
                                         'product_id': product_id,
                                         'owner_id': owner_id,
                                         'title': '反馈标题',
                                         'description': 'description'
                                     },
                                     headers={'Authentication': token})
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        # 再次创建
        error_response1 = await client.post(url,
                                            json={
                                                'product_id': product_id,
                                                'owner_id': owner_id,
                                                'title': '反馈标题'
                                            },
                                            headers={'Authentication': token})
        assert error_response1.status == 200

        error_result1 = await error_response1.json()
        assert error_result1['error_type'] == 'issue_already_exist'
        assert error_result1['message'] == '您已经反馈过相关问题了'

        # 用其他身份反馈
        error_response2 = await client.post(url,
                                            json={
                                                'product_id': product_id,
                                                'owner_id': owner_id,
                                                'title': '反馈标题'
                                            },
                                            headers={
                                                'Authentication':
                                                await AccountService.get_token(
                                                    client,
                                                    app.config.ROLE_DEVELOPER)
                                            })
        assert error_response2.status == 200

        error_result2 = await error_response2.json()
        assert error_result2['error_type'] == 'permission_denied'
        assert error_result2['message'] == '没有权限'

        return {
            '正确响应': json_result,
            '错误响应': error_result1,
            '权限验证错误': error_result2
        }
