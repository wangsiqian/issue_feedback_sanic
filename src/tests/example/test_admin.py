class TestAdmin:
    async def test_list_admin(self, client):
        request_body = {'example_field': 'example'}
        response1 = await client.post('/v1/example', json=request_body)
        assert response1.status == 200

        response = await client.get('/admin/example')
        assert response.status == 200
