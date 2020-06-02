from issue.exceptions import IssueNotFound, StatisticsNotFount
from issue.models.issue import (Issue, IssueByProduct, IssueVoteRecord,
                                IssueVoteStatistics)
from issue.models.serializers import (
    AssignIssueSerializer, CreateIssueSerializer, IssueIdSerializer,
    IssueSerializer, IssueVoteRecordSerializer, IssueVoteSerializer,
    MultiQueryIssuesSerializer, StatisticsSerializer, UpdateIssueTagSerializer)
from libs.sanic_api.views import (GetView, ListView, PostView, PutView,
                                  ok_response)


class CreateIssueService(PostView):
    """创建反馈
    """
    args_deserializer_class = CreateIssueSerializer
    post_serializer_class = IssueSerializer

    async def save(self):
        return await Issue.new(product_id=self.validated_data['product_id'],
                               owner_id=self.validated_data['owner_id'],
                               title=self.validated_data['title'],
                               description=self.validated_data['description'])


class ListIssuesByProductIdService(ListView):
    """根据产品信息获取反馈
    """
    args_deserializer_class = MultiQueryIssuesSerializer
    list_serializer_class = IssueSerializer

    async def get_issues(self):
        # 查询该产品下有哪些 issue
        issues_by_product = await IssueByProduct.objects.filter(
            product_id=self.validated_data['product_id']).async_all()

        issues = []
        for issue_by_product in issues_by_product:
            try:
                issue = await Issue.async_get(
                    issue_id=issue_by_product.issue_id,
                    status=self.validated_data['status'])
            except Issue.DoesNotExist:
                continue

            issues.append(issue)

        # 排序
        sorted_issues = sorted(issues,
                               key=lambda _issue: _issue.created_at,
                               reverse=True)
        return sorted_issues

    async def filter_objects(self):
        issues = await self.get_issues()

        result = {'issues': [], 'count': len(issues)}
        # 分页
        start = self.validated_data.get('start', 0)
        limit = self.validated_data.get('limit', 10)
        serializer = self.list_serializer_class()
        for issue in issues[start:start + limit]:
            issue_map = serializer.dump(issue)
            # 获取统计信息
            try:
                statistics = await IssueVoteStatistics.async_get(
                    issue_id=issue.issue_id)
            except IssueVoteStatistics.DoesNotExist:
                issue_map.update({'likes': 0, 'dislikes': 0})
            else:
                issue_map.update({
                    'likes': statistics.likes,
                    'dislikes': statistics.dislikes,
                })
            result['issues'].append(issue_map)

        return result

    def response(self, result):
        return ok_response(result)


class IssueVoteService(PutView):
    """反馈投票服务
    """
    args_deserializer_class = IssueVoteSerializer
    put_serializer_class = IssueVoteRecordSerializer

    async def save(self):
        issue_id = self.validated_data['issue_id']
        user_id = self.validated_data['user_id']
        opinion = self.validated_data['opinion']
        try:
            record = await IssueVoteRecord.async_get(issue_id=issue_id,
                                                     user_id=user_id)
        except IssueVoteRecord.DoesNotExist:
            return await IssueVoteRecord.new_record(issue_id=issue_id,
                                                    user_id=user_id,
                                                    opinion=opinion)

        # 已存在则更新数据
        await record.update_record(issue_id=issue_id, opinion=opinion)
        return record


class GetStatisticsByIssueIdService(GetView):
    """获取反馈的统计数据
    """
    args_deserializer_class = IssueIdSerializer
    get_serializer_class = StatisticsSerializer

    async def get_object(self):
        try:
            return await IssueVoteStatistics.async_get(
                issue_id=self.validated_data['issue_id'])
        except IssueVoteStatistics.DoesNotExist:
            raise StatisticsNotFount


class AssignIssueService(PutView):
    """分配 issue
    """
    args_deserializer_class = AssignIssueSerializer
    put_serializer_class = IssueSerializer

    async def save(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        await issue.handle_developer(self.validated_data['developer_id'])
        await issue.async_save()

        return issue


class UpdateIssueTagService(PutView):
    """更新 issue 的标签
    """
    args_deserializer_class = UpdateIssueTagSerializer
    put_serializer_class = None

    async def save(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        await issue.handle_tags(self.validated_data['tags_name'])

        return issue


class GetIssueById(GetView):
    """通过 issue id 获取 issue
    """
    args_deserializer_class = IssueIdSerializer
    get_serializer_class = IssueSerializer

    async def get_object(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        return issue
