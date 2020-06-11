from comment.models.comment import Comment
from comment.models.serializers import (CommentSerializer,
                                        CreateCommentSerializer,
                                        ListCommentsSerializer)
from issue.models.serializers import IssueIdSerializer
from libs.sanic_api.views import ListView, PostView


class CreateCommentService(PostView):
    """创建评论
    """
    args_deserializer_class = CreateCommentSerializer
    post_serializer_class = CommentSerializer

    async def save(self):
        return await Comment.new(
            user_id=self.validated_data['user_id'],
            issue_id=self.validated_data['issue_id'],
            content=self.validated_data['content'],
            receiver_id=self.validated_data['receiver_id'])


class ListCommentsByIssueIdService(ListView):
    """列出评论
    """
    list_result_name = 'comments'
    args_deserializer_class = IssueIdSerializer
    list_serializer_class = ListCommentsSerializer

    async def filter_objects(self):
        comments = await Comment.objects.filter(
            issue_id=self.validated_data['issue_id']).async_all()
        return sorted(comments, key=lambda comment: comment.created_at)
