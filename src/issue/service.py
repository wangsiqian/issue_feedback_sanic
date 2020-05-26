from issue.exceptions import StatisticsNotFount
from issue.models.issue import (Issue, IssueByProduct, IssueVoteRecord,
                                IssueVoteStatistics)
from issue.models.serializers import (CreateIssueSerializer, IssueIdSerializer,
                                      IssueSerializer,
                                      IssueVoteRecordSerializer,
                                      IssueVoteSerializer,
                                      MultiQueryIssuesSerializer,
                                      StatisticsSerializer)
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
    list_result_name = 'issues'
    args_deserializer_class = MultiQueryIssuesSerializer
    list_serializer_class = IssueSerializer

    async def filter_objects(self):
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

    def response(self, results):
        # 分页
        start = self.validated_data.get('start', 0)
        limit = self.validated_data.get('limit', 10)

        _serializer = self.list_serializer_class()
        return ok_response({
            self.list_result_name:
            _serializer.dump(results[start:start + limit], many=True),
            'count':
            len(results)
        })


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
