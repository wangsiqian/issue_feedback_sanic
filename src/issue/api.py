from issue.service import CreateIssueService, IssueVoteService


class CreateIssueApi(CreateIssueService):
    post_serializer_class = None


class IssueVoteApi(IssueVoteService):
    put_serializer_class = None
