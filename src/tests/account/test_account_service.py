class TestAccountService:
    async def test_create_account(self, client, rabbitmq_consumer):
        url = '/service/v1/account'
        response = await client.post(url,
                                     json={
                                         'account_id': '123456789@qq.com',
                                         'password': '123456789@qq.com'
                                     })

        assert response.status == 200

        message = rabbitmq_consumer.get_one()
        assert message.get('user_id')
        assert message.get('event') == 'create_profile'
