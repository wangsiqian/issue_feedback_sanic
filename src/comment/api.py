from comment.service import CreateCommentService, ListCommentsByIssueIdService
from libs.sanic_api.exceptions import PermissionDenied


class CreateCommentApi(CreateCommentService):
    async def save(self):
        if self.validated_data['user_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()


class ListCommentsByIssueIdApi(ListCommentsByIssueIdService):
    pass
