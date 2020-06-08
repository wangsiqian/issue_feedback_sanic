from issue.models.serializers import IssueIdSerializer
from issue.service import (AssignIssueService, CreateIssueService,
                           GetIssueByIdService, IssueVoteService,
                           ListDevelopersByIssueService,
                           ListIssuesByProductIdService,
                           ModifyIssueStatusService, UpdateIssueTagService)


class CreateIssueApi(CreateIssueService):
    post_serializer_class = IssueIdSerializer


class IssueVoteApi(IssueVoteService):
    put_serializer_class = None


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
    pass
