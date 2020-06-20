from random import randint

from tests.docs import api_docs


class AccountApi:
    @classmethod
    async def create_account(cls, client, account_id, password):
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})

        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        # 创建账号
        response = await client.post('/service/v1/account',
                                     json={
                                         'account_id': account_id,
                                         'password': password,
                                         'validate_token': validate_token,
                                         'validate_code': validate_code
                                     })
        assert response.status == 200


class TestAccountApi:
    @api_docs(title='发送验证码',
              path='/v1/account/send_code',
              method='POST',
              body={'account_id（必填）': '邮箱'})
    async def test_send_code(self, client):
        """验证发送验证码"""
        response = await client.post('/v1/account/send_code',
                                     json={'account_id': '123456@qq.com'})

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        # 再次发送
        error_response = await client.post(
            '/service/v1/account/send_code',
            json={'account_id': '123456@qq.com'})

        assert error_response.status == 200
        error_result = await error_response.json()
        assert error_result['error_type'] == 'code_already_sent'
        assert error_result['message'] == '验证码已经发送'
        return {'正确响应': json_result, '权限验证错误': error_result}

    @api_docs(title='创建帐号',
              path='/v1/account',
              method='POST',
              body={
                  'account_id（必填）': '邮箱',
                  'password(密码)': '密码',
                  'validate_token': 'token',
                  'validate_code': '验证码'
              })
    async def test_create_account(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com',
                                         'validate_token': validate_token,
                                         'validate_code': validate_code,
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']
        # 再次创建
        error_response1 = await client.post(url,
                                            json={
                                                'account_id': account_id,
                                                'password': '123456789@qq.com',
                                                'validate_token':
                                                validate_token,
                                                'validate_code': validate_code,
                                            })
        assert error_response1.status == 200

        error_result1 = await error_response1.json()
        assert error_result1['error_type'] == 'account_already_exist'
        assert error_result1['message'] == '该账号已经存在，请登录'

        return {
            '正确响应': json_result,
            '帐号已存在': error_result1,
        }

    @api_docs(title='登录帐号',
              path='/v1/login',
              method='POST',
              body={
                  'account_id（必填）': '邮箱',
                  'password（必填）': '密码'
              })
    async def test_login(self, client):
        # 创建账号
        account_id = '123456789@qq.com'
        password = '123456789@qq.com'
        # 创建账号
        await AccountApi.create_account(client, account_id, password)
        response = await client.post('/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })
        assert response.status == 200

        json_result = await response.json()

        assert json_result['ok']
        assert json_result['result']['token']
        assert json_result['result']['user_id']
        assert json_result['result']['role_id'] == 'USER'

        # 错误的密码
        error_response = await client.post('/v1/login',
                                           json={
                                               'account_id':
                                               '123456789@qq.com',
                                               'password': '6789@qq.com'
                                           })
        error_result = await error_response.json()
        assert error_result['error_type'] == 'password_wrong'
        assert error_result['message'] == '密码错误'

        return {'正确响应': json_result, '密码错误': error_result}
