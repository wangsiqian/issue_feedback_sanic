from statistics.service import (CountIssueByDeveloperService,
                                CountIssueByManagerService,
                                CountIssueByUserService)

from libs.sanic_api.exceptions import PermissionDenied


class CountIssueByUserApi(CountIssueByUserService):
    async def get_object(self):
        if self.validated_data['owner_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().get_object()


class CountIssueByDeveloperApi(CountIssueByDeveloperService):
    async def get_object(self):
        if self.validated_data['developer_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().get_object()


class CountIssueByManagerApi(CountIssueByManagerService):
    async def get_object(self):
        if self.validated_data['manager_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().get_object()
