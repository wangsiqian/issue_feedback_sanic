from product.service import CreateProductService, ListProductByManagerService


class CreateProductApi(CreateProductService):
    post_serializer_class = None


class ListProductByManagerIdApi(ListProductByManagerService):
    pass
