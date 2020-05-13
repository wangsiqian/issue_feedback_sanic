from issue.service import CreateIssueService


class CreateIssueApi(CreateIssueService):
    post_serializer_class = None
