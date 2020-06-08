from product.service import (CreateProductService, ListProductByManagerService,
                             ListProductsService, UpdateProductByIdService,
                             DeleteProductByIdService)


class CreateProductApi(CreateProductService):
    pass


class ListProductsApi(ListProductsService):
    pass


class ListProductByManagerIdApi(ListProductByManagerService):
    pass


class UpdateProductByIdApi(UpdateProductByIdService):
    pass


class DeleteProductByIdApi(DeleteProductByIdService):
    pass
