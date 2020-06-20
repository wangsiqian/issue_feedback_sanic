from libs.sanic_api.exceptions import PermissionDenied
from product.service import (CreateProductService, DeleteProductByIdService,
                             ListProductByManagerService, ListProductsService,
                             UpdateProductByIdService)


class CreateProductApi(CreateProductService):
    async def save(self):
        if self.validated_data['manager_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class ListProductsApi(ListProductsService):
    pass


class ListProductByManagerIdApi(ListProductByManagerService):
    async def filter_objects(self):
        if self.validated_data['manager_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().filter_objects()


class UpdateProductByIdApi(UpdateProductByIdService):
    async def save(self):
        if self.validated_data['manager_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class DeleteProductByIdApi(DeleteProductByIdService):
    async def save(self):
        if self.validated_data['manager_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()
