from product.service import CreateProductService


class CreateProductApi(CreateProductService):
    post_serializer_class = None
