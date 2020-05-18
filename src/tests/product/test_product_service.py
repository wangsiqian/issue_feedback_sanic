import uuid


class TestProductService:
    async def _create_product(self, client, manager_id):
        # 创建一个产品
        response = await client.post('/service/v1/product',
                                     json={
                                         'manager_id': manager_id,
                                         'name': '产品1',
                                         'description': '产品1的介绍'
                                     })
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return json_result['result']['product_id']

    async def test_create_product(self, client):
        url = '/service/v1/product'

        manager_id = str(uuid.uuid4())
        response = await client.post(url,
                                     json={
                                         'manager_id': manager_id,
                                         'name': '产品1',
                                         'description': '产品1的介绍'
                                     })
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        product = json_result['result']
        assert product['manager_id'] == manager_id
        assert product['name'] == '产品1'
        assert product['description'] == '产品1的介绍'

        assert product['product_id']
        assert product['created_at']

    async def test_list_products(self, client):
        """测试列出产品"""
        manager_id = str(uuid.uuid4())
        # 创建3个产品
        await self._create_product(client, manager_id)
        await self._create_product(client, manager_id)
        await self._create_product(client, manager_id)

        response = await client.get(f'/service/v1/products')
        assert response.status == 200

        json_result = await response.json()
        assert json_result['ok']

        products = json_result['result']['products']
        print(products)
        assert len(products) == 3

    async def test_list_products_by_manager(self, client):
        manager1_id = str(uuid.uuid4())
        # 创建3个产品
        await self._create_product(client, manager1_id)
        await self._create_product(client, manager1_id)
        await self._create_product(client, manager1_id)

        # 另一个管理员
        manager2_id = str(uuid.uuid4())
        await self._create_product(client, manager2_id)

        # 按管理员ID查询
        response1 = await client.get(
            f'/service/v1/product/manager/{manager1_id}')
        assert response1.status == 200
        json_result1 = await response1.json()
        assert json_result1['ok']

        products = json_result1['result']['products']
        assert products[0]['manager_id'] == manager1_id
        assert len(products) == 3

        response2 = await client.get(
            f'/service/v1/product/manager/{manager2_id}')
        json_result2 = await response2.json()
        products = json_result2['result']['products']
        assert products[0]['manager_id'] == manager2_id
        assert len(products) == 1
