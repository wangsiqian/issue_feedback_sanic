from comment.models.serializers import CommentIdSerializer
from comment.service import CreateCommentService, ListCommentsByIssueIdService


class CreateCommentApi(CreateCommentService):
    post_serializer_class = CommentIdSerializer


class ListCommentsByIssueIdApi(ListCommentsByIssueIdService):
    pass
