from profile.models.profile import Profile

from app import app
from issue.exceptions import IssueNotFound, StatisticsNotFount
from issue.models.issue import (Issue, IssueByProduct, IssueByUser,
                                IssueVoteRecord, IssueVoteStatistics)
from issue.models.serializers import (AssignIssueSerializer,
                                      CreateIssueSerializer,
                                      DeveloperSerializer,
                                      IssueIdAndUserIdSerializer,
                                      IssueIdSerializer, IssueSerializer,
                                      IssueVoteRecordSerializer,
                                      IssueVoteSerializer,
                                      ListIssueByUserSerializer,
                                      ListIssuesSerializer,
                                      ModifyIssueStatusSerializer,
                                      MultiGetDeveloperSerializer,
                                      MultiQueryIssuesSerializer,
                                      OpinionSerializer, StatisticsSerializer,
                                      UpdateIssueSerializer,
                                      UpdateIssueTagSerializer)
from libs.sanic_api.exceptions import PermissionDenied
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
        start = self.validated_data.get('start')
        limit = self.validated_data.get('limit')
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

        await issue.handle_developers(self.validated_data['developer_ids'])

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


class GetIssueByIdService(GetView):
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


class ModifyIssueStatusService(PutView):
    """修改 issue 状态
    """
    args_deserializer_class = ModifyIssueStatusSerializer

    async def save(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        user_id = self.validated_data['user_id']
        # 获取身份
        role_id = await Profile.get_role_id(user_id=user_id)

        admin_role = [app.config.ROLE_DEVELOPER, app.config.ROLE_MANAGER]
        if issue.owner_id != user_id and role_id not in admin_role:
            # 判断是否有关闭的权限
            raise PermissionDenied

        status = self.validated_data['status']
        if status == issue.STATUS_OPENING:
            await issue.open_issue()
        elif status == issue.STATUS_CLOSED:
            await issue.close_issue()

        return issue


class ListDevelopersByIssueService(ListView):
    """列出某个反馈里面没有被选中的开发人员
    """
    args_deserializer_class = MultiGetDeveloperSerializer
    list_serializer_class = DeveloperSerializer

    async def get_developers(self):
        nickname = self.validated_data['nickname']
        if nickname:
            rows = await app.cassandra.execute_future(
                """
                SELECT *
                FROM profile
                WHERE role_id = %s
                AND nickname LIKE %s ALLOW FILTERING
                """, (app.config.ROLE_DEVELOPER, f'%{nickname}%'))
        else:
            rows = await Profile.objects.filter(
                role_id=app.config.ROLE_DEVELOPER).async_all()

        return list(rows)

    async def filter_objects(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        developers = await self.get_developers()
        for developer_id in issue.developer_ids:
            # 移除已经被选中的developer
            try:
                profile = await Profile.async_get(user_id=developer_id)
            except Profile.DoesNotExist:
                continue

            try:
                developers.remove(profile)
            except ValueError:
                pass

        return developers

    def response(self, results):
        _serializer = self.list_serializer_class()
        start = self.validated_data.get('start')
        limit = self.validated_data.get('limit')
        profile = results[start:start + limit]
        return ok_response({
            'developers': _serializer.dump(profile, many=True),
            'count': len(results)
        })


class UpdateIssueService(PutView):
    """更新需求
    """
    args_deserializer_class = UpdateIssueSerializer

    async def save(self):
        try:
            issue = await Issue.async_get(
                issue_id=self.validated_data['issue_id'])
        except Issue.DoesNotExist:
            raise IssueNotFound

        if self.validated_data['owner_id'] != issue.owner_id:
            raise PermissionDenied

        await issue.update_content(**self.validated_data)


class GetUserOpinionByIdService(GetView):
    """获取用户对该需求的观点
    """
    args_deserializer_class = IssueIdAndUserIdSerializer
    get_serializer_class = OpinionSerializer

    async def get_object(self):
        try:
            record = await IssueVoteRecord.async_get(
                issue_id=self.validated_data['issue_id'],
                user_id=self.validated_data['user_id'])
        except IssueVoteRecord.DoesNotExist:
            return {'opinion': IssueVoteRecord.OPINION_NONE}

        return record


class ListIssuesByOwnerIdService(ListView):
    """用户个人中心列出自己创建的需求
    """
    list_result_name = 'issues'
    args_deserializer_class = ListIssueByUserSerializer
    list_serializer_class = ListIssuesSerializer

    async def filter_objects(self):
        issues_by_user = await IssueByUser.objects.filter(
            owner_id=self.validated_data['owner_id']).async_all()
        start = self.validated_data['start']
        limit = self.validated_data['limit']
        paged_issues = issues_by_user[start:start + limit]

        issues = []
        status = self.validated_data.get('status')
        for issue_by_user in paged_issues:
            try:
                issue = await Issue.async_get(issue_id=issue_by_user.issue_id)
            except Issue.DoesNotExist:
                continue

            if status:
                if issue.status == status:
                    # 按状态过滤
                    issues.append(issue)
            else:
                issues.append(issue)

        return issues
