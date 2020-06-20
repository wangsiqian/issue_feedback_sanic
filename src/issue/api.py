from issue.models.serializers import IssueIdSerializer
from issue.service import (AssignIssueService, CreateIssueService,
                           GetIssueByIdService, GetUserOpinionByIdService,
                           IssueVoteService, ListDevelopersByIssueService,
                           ListIssuesByOwnerIdService,
                           ListIssuesByProductIdService,
                           ModifyIssueStatusService, UpdateIssueService,
                           UpdateIssueTagService)
from libs.sanic_api.exceptions import PermissionDenied


class CreateIssueApi(CreateIssueService):
    post_serializer_class = IssueIdSerializer

    async def save(self):
        if self.validated_data['owner_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class IssueVoteApi(IssueVoteService):
    put_serializer_class = None

    async def save(self):
        if self.validated_data['user_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class ListIssuesByProductIdApi(ListIssuesByProductIdService):
    pass


class AssignIssueApi(AssignIssueService):
    put_serializer_class = None


class UpdateIssueTagApi(UpdateIssueTagService):
    pass


class GetIssueByIdApi(GetIssueByIdService):
    pass


class ListDevelopersByIssueApi(ListDevelopersByIssueService):
    pass


class ModifyIssueStatusApi(ModifyIssueStatusService):
    async def save(self):
        if self.validated_data['user_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class UpdateIssueApi(UpdateIssueService):
    async def save(self):
        if self.validated_data['owner_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class GetUserOpinionByIdApi(GetUserOpinionByIdService):
    pass


class ListIssuesByOwnerIdApi(ListIssuesByOwnerIdService):
    async def filter_objects(self):
        if self.validated_data['owner_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().filter_objects()
