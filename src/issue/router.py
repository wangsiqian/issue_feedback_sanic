"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from app import app
from issue import api, service
###############################
# api
###############################
from libs.jwt import jwt_wrapper

config = app.config

issue_api_blueprint = Blueprint('issue_api', version='1')

api_urls = [('/issue', jwt_wrapper(api.CreateIssueApi.as_view(),
                                   required=True), ['POST']),
            ('/issue/<issue_id>', api.GetIssueByIdApi.as_view(), ['GET']),
            ('/issue/<issue_id>',
             jwt_wrapper(api.UpdateIssueApi.as_view(),
                         required=True), ['PUT']),
            ('/issue/<issue_id>/vote',
             jwt_wrapper(api.IssueVoteApi.as_view(), required=True), ['PUT']),
            ('/issue/product/<product_id>',
             api.ListIssuesByProductIdApi.as_view(), ['GET']),
            ('/issue/<issue_id>/assign',
             jwt_wrapper(api.AssignIssueApi.as_view(),
                         role_ids=(
                             config.ROLE_DEVELOPER,
                             config.ROLE_MANAGER,
                         )), ['PUT']),
            ('/issue/<issue_id>/tag',
             jwt_wrapper(api.UpdateIssueTagApi.as_view(),
                         role_ids=(config.ROLE_MANAGER, )), ['PUT']),
            ('/issue/<issue_id>/developers',
             jwt_wrapper(api.ListDevelopersByIssueApi.as_view(),
                         role_ids=(
                             config.ROLE_DEVELOPER,
                             config.ROLE_MANAGER,
                         )), ['GET']),
            ('/issue/<issue_id>/status',
             jwt_wrapper(api.ModifyIssueStatusApi.as_view(),
                         required=True), ['PUT']),
            ('/issue/<issue_id>/user/<user_id>/opinion',
             jwt_wrapper(api.GetUserOpinionByIdApi.as_view(),
                         required=True), ['GET']),
            ('/issue/owner/<owner_id>',
             jwt_wrapper(api.ListIssuesByOwnerIdApi.as_view(),
                         role_ids=(config.ROLE_USER, )), ['GET'])]
for url, view, methods in api_urls:
    issue_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [
    ('/issue', service.CreateIssueService.as_view(), ['POST']),
    ('/issue/<issue_id>', service.GetIssueByIdService.as_view(), ['GET']),
    ('/issue/<issue_id>', service.UpdateIssueService.as_view(), ['PUT']),
    ('/issue/<issue_id>/vote', service.IssueVoteService.as_view(), ['PUT']),
    ('/issue/<issue_id>/statistics',
     service.GetStatisticsByIssueIdService.as_view(), ['GET']),
    ('/issue/product/<product_id>',
     service.ListIssuesByProductIdService.as_view(), ['GET']),
    ('/issue/<issue_id>/assign', service.AssignIssueService.as_view(), ['PUT'
                                                                        ]),
    ('/issue/<issue_id>/tag', service.UpdateIssueTagService.as_view(), ['PUT'
                                                                        ]),
    ('/issue/<issue_id>/developers',
     service.ListDevelopersByIssueService.as_view(), ['GET']),
    ('/issue/<issue_id>/status', service.ModifyIssueStatusService.as_view(),
     ['PUT']),
    ('/issue/<issue_id>/user/<user_id>/opinion',
     service.GetUserOpinionByIdService.as_view(), ['GET']),
    ('/issue/owner/<owner_id>', service.ListIssuesByOwnerIdService.as_view(),
     ['GET'])
]
issue_service_blueprint = Blueprint('issue_service', url_prefix='/service/v1')
for url, view, methods in service_urls:
    issue_service_blueprint.add_route(view, url, methods=methods)
