from issue.exceptions import IssueAlreadyExist
from issue.models.issue import Issue
from issue.models.serializers import CreateIssueSerializer, IssueSerializer
from libs.sanic_api.views import PostView


class CreateIssueService(PostView):
    """创建反馈
    """
    args_deserializer_class = CreateIssueSerializer
    post_serializer_class = IssueSerializer

    async def save(self):
        product_id = self.validated_data['product_id']
        owner_id = self.validated_data['owner_id']
        title = self.validated_data['title']
        try:
            await Issue.async_get(product_id=product_id,
                                  owner_id=owner_id,
                                  title=title)
        except Issue.DoesNotExist:
            return await Issue.new(
                product_id=product_id,
                owner_id=owner_id,
                title=title,
                description=self.validated_data['description'])

        raise IssueAlreadyExist
