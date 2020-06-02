from random import randint

from tests.profile.test_profile_service import ProfileService


class AccountService:
    @classmethod
    async def create_account(cls, client, account_id, password, role_id):
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
                                         'validate_code': validate_code,
                                         'role_id': role_id
                                     })
        assert response.status == 200

    @classmethod
    async def get_token(cls, client, role_id):
        account_id = str(randint(1, 999999)).zfill(6) + '@qq.com'
        password = '123456789@qq.com'
        # 创建账号
        await AccountService.create_account(client, account_id, password,
                                            role_id)

        # 登陆
        response = await client.post('/service/v1/login',
                                     json={
                                         'account_id': account_id,
                                         'password': password
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']['token']


class TestAccountService:
    async def test_send_code(self, client):
        """验证发送验证码"""

        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': '123456@qq.com'})

        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']
        assert len(json_result['result']['validate_code']) == 6

        # 再次发送
        error_response = await client.post(
            '/service/v1/account/send_code',
            json={'account_id': '123456@qq.com'})

        assert error_response.status == 200
        error_result = await error_response.json()
        assert error_result['error_type'] == 'code_already_sent'
        assert error_result['message'] == '验证码已经发送'

    async def test_create_account(self, client):
        account_id = '123456789@qq.com'
        # 获取验证码
        response = await client.post('/service/v1/account/send_code',
                                     json={'account_id': account_id})
        assert response.status == 200
        json_result = await response.json()
        validate_token = json_result['result']['validate_token']
        validate_code = json_result['result']['validate_code']

        url = '/service/v1/account'
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

    async def test_login(self, client):
        account_id = '123456789@qq.com'
        password = '123456789@qq.com'
        # 创建账号
        await AccountService.create_account(client, account_id, password,
                                            'USER')

        # 登陆
        response = await client.post('/service/v1/login',
                                     json={
                                         'account_id': account_id,
                                         'password': password
                                     })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']
        assert json_result['result']['token']
        assert json_result['result']['user_id']
        assert json_result['result']['role_id'] == 'USER'

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
