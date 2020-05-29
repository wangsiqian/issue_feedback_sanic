from issue.service import (AssignIssueService, CreateIssueService,
                           IssueVoteService, ListIssuesByProductIdService)


class CreateIssueApi(CreateIssueService):
    post_serializer_class = None


class IssueVoteApi(IssueVoteService):
    put_serializer_class = None


class ListIssuesByProductIdApi(ListIssuesByProductIdService):
    pass


class AssignIssueApi(AssignIssueService):
    put_serializer_class = None
