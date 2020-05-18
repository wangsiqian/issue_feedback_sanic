from product.service import (CreateProductService, ListProductByManagerService,
                             ListProductsService)


class CreateProductApi(CreateProductService):
    post_serializer_class = None


class ListProductsApi(ListProductsService):
    pass


class ListProductByManagerIdApi(ListProductByManagerService):
    pass
