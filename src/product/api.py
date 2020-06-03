from product.models.serializers import ProductIdSerializer
from product.service import (CreateProductService, ListProductByManagerService,
                             ListProductsService)


class CreateProductApi(CreateProductService):
    post_serializer_class = ProductIdSerializer


class ListProductsApi(ListProductsService):
    pass


class ListProductByManagerIdApi(ListProductByManagerService):
    pass
