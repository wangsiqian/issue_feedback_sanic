import uuid

from tests.account.test_account_service import AccountService
from tests.docs import api_docs

from app import app


class TestProductApi:
    async def _create_product(self, client, manager_id, name, description):
        # 创建一个产品
        token = await AccountService.get_token(client, app.config.ROLE_MANAGER)
        response = await client.post('/v1/product',
                                     json={
                                         'manager_id': manager_id,
                                         'name': name,
                                         'description': description
                                     },
                                     headers={'Authorization': token})
        assert response.status == 200
        json_result = await response.json()
        assert json_result['ok']

        return json_result

    @api_docs(title='创建一个产品',
              path='/v1/product',
              method='POST',
              body={
                  'manager_id（必填）': 'manager_ID',
                  'name（必填）': '产品名',
                  'description': '产品介绍'
              },
              headers={'Authorization': '用户 Token'})
    async def test_create_product(self, client):
        url = '/v1/product'
        token = await AccountService.get_token(client, app.config.ROLE_MANAGER)
        manager_id = str(uuid.uuid4())
        response = await client.post(url,
                                     json={
                                         'manager_id': manager_id,
                                         'name': '产品1',
                                         'description': '产品1的介绍'
                                     },
                                     headers={'Authorization': token})
        assert response.status == 200
        json_result = await response.json()
        print(json_result)
        assert json_result['ok']

        return {'正确响应': json_result}

    @api_docs(title='查询产品',
              path='/v1/product/manager/{manager_id}',
              method='GET',
              headers={'Authorization': '用户 Token'})
    async def test_list_products(self, client):
        manager1_id = str(uuid.uuid4())
        token = await AccountService.get_token(client, app.config.ROLE_MANAGER)
        # 创建3个产品
        await self._create_product(client, manager1_id, '1', '1')
        await self._create_product(client, manager1_id, '2', '2')
        await self._create_product(client, manager1_id, '3', '3')

        # 另一个管理员
        manager2_id = str(uuid.uuid4())
        await self._create_product(client, manager2_id, '4', '4')

        # 按管理员ID查询
        response1 = await client.get(f'/v1/product/manager/{manager1_id}',
                                     headers={'Authorization': token})
        assert response1.status == 200
        json_result1 = await response1.json()
        assert json_result1['ok']

        products = json_result1['result']['products']
        assert products[0]['manager_id'] == manager1_id
        assert len(products) == 3

        response2 = await client.get(f'/v1/product/manager/{manager2_id}',
                                     headers={'Authorization': token})
        json_result2 = await response2.json()
        products = json_result2['result']['products']
        assert products[0]['manager_id'] == manager2_id
        assert len(products) == 1

        return {'正确响应': json_result2}
