from product.service import (CreateProductService, DeleteProductByIdService,
                             ListProductByManagerService, ListProductsService,
                             UpdateProductByIdService)


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
