from statistics.serializers import OwnerIdSerializer, UserCounterSerializer

from issue.models.issue import Issue, IssueByUser
from libs.sanic_api.views import GetView


class CountIssueByUserService(GetView):
    """统计用户提出的反馈和已处理的反馈
    """
    args_deserializer_class = OwnerIdSerializer
    get_serializer_class = UserCounterSerializer

    async def get_object(self):
        issues_by_user = await IssueByUser.objects.filter(
            owner_id=self.validated_data['owner_id']).async_all()
        total_count = len(issues_by_user)

        solved_count = 0
        for issues_by_user in issues_by_user:
            try:
                issue = await Issue.async_get(issue_id=issues_by_user.issue_id)
            except Issue.DoesNotExist:
                continue

            if issue.status == issue.STATUS_CLOSED:
                # 已经关闭的需求
                solved_count += 1

        return {'total_count': total_count, 'solved_count': solved_count}
