from random import randint


class AccountService:
    @classmethod
    async def get_token(cls, client, role_id):
        # 创建账号
        account_id = str(randint(0, 999999)).zfill(6) + '@qq.com'
        await client.post('/service/v1/account',
                          json={
                              'account_id': account_id,
                              'password': '123456789@qq.com',
                              'role_id': role_id
                          })

        # 登陆
        response = await client.post('/service/v1/login',
                                     json={
                                         'account_id': account_id,
                                         'password': '123456789@qq.com'
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']['token']


class TestAccountService:
    async def test_create_account(self, client):
        url = '/service/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

    async def test_login(self, client):
        # 创建账号
        response = await client.post('/service/v1/account',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com',
                                         'role_id': '01'
                                     })

        # 登陆
        response = await client.post('/service/v1/login',
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })
        assert response.status == 200

        json_result = await response.json()
        print(json_result)

        assert json_result['ok']
        assert json_result['result']['token']
        assert json_result['result']['user_id']
        assert json_result['result']['role_id'] == '01'

        # 错误的密码
        error_response = await client.post('/service/v1/login',
                                           json={
                                               'account_id':
                                               '123456789@qq.com',
                                               'password': '6789@qq.com'
                                           })
        error_result = await error_response.json()
        assert error_result['error_type'] == 'password_wrong'
        assert error_result['message'] == '密码错误'
