from libs.sanic_api.views import DeleteView, ListView, PostView, PutView
from product.exceptions import ProductAlreadyExist, ProductNotFound
from product.models.product import Product
from product.models.serializers import (CreateProductSerializer,
                                        DeleteProductSerializer,
                                        ManagerIdSerializer, ProductSerializer,
                                        UpdateProductSerializer)


class CreateProductService(PostView):
    """创建产品
    """
    args_deserializer_class = CreateProductSerializer
    post_serializer_class = ProductSerializer

    async def save(self):
        name = self.validated_data['name']
        try:
            await Product.async_get(name=name)
        except Product.DoesNotExist:
            return await Product.new(
                manager_id=self.validated_data['manager_id'],
                name=name,
                description=self.validated_data['description'])

        raise ProductAlreadyExist


class ListProductsService(ListView):
    args_deserializer_class = None
    list_serializer_class = ProductSerializer
    list_result_name = 'products'

    async def filter_objects(self):
        return await Product.async_all()


class ListProductByManagerService(ListView):
    """根据管理人ID列出产品
    """
    args_deserializer_class = ManagerIdSerializer
    list_serializer_class = ProductSerializer
    list_result_name = 'products'

    async def filter_objects(self):
        products = await Product.objects.filter(
            manager_id=self.validated_data['manager_id']).async_all()

        return sorted(products,
                      key=lambda product: product.created_at,
                      reverse=True)


class DeleteProductByIdService(DeleteView):
    """删除产品
    """
    args_deserializer_class = DeleteProductSerializer

    async def save(self):
        try:
            product = await Product.async_get(
                manager_id=self.validated_data['manager_id'],
                product_id=self.validated_data['product_id'])
        except Product.DoesNotExist:
            raise ProductNotFound

        await product.async_delete()


class UpdateProductByIdService(PutView):
    """更新产品
    """
    args_deserializer_class = UpdateProductSerializer
    put_serializer_class = ProductSerializer

    async def save(self):
        try:
            product = await Product.async_get(
                manager_id=self.validated_data['manager_id'],
                product_id=self.validated_data['product_id'])
        except Product.DoesNotExist:
            raise ProductNotFound

        return await product.update_product(**self.validated_data)
