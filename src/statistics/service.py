from statistics.serializers import (DeveloperCounterSerializer,
                                    DeveloperIdSerializer, OwnerIdSerializer,
                                    UserCounterSerializer)

from issue.models.issue import Issue, IssueByDeveloper, IssueByUser
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


class CountIssueByDeveloperService(GetView):
    """统计开发人员正在处理和已经处理的需求
    """
    args_deserializer_class = DeveloperIdSerializer
    get_serializer_class = DeveloperCounterSerializer

    async def get_object(self):
        issues_by_developer = await IssueByDeveloper.objects.filter(
            developer_id=self.validated_data['developer_id'], ).async_all()
        closed_count = 0
        opening_count = 0
        for issue_by_developer in issues_by_developer:
            try:
                issue = await Issue.async_get(
                    issue_id=issue_by_developer.issue_id)
            except Issue.DoesNotExist:
                continue

            if issue.status == issue.STATUS_CLOSED:
                closed_count += 1
            elif issue.status == issue.STATUS_OPENING:
                opening_count += 1

        return {'opening_count': opening_count, 'closed_count': closed_count}
