class TestService:
    """测试内部服务API
    """
    async def test_service_api(self, client):
        """测试使用 service api
        """
        url = '/service/v1/example/example'
        response = await client.get(url)
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok'] is True
