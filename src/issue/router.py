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

issue_api_blueprint = Blueprint('issue_api', version='1')

api_urls = [('/issue',
             jwt_wrapper(api.CreateIssueApi.as_view(),
                         role_ids=(app.config.ROLE_USER, )), ['POST']),
            ('/issue/<issue_id>/user/<user_id>/vote',
             jwt_wrapper(api.IssueVoteApi.as_view(),
                         role_ids=(app.config.ROLE_USER, )), ['PUT']),
            ('/issue/product/<product_id>/opening',
             api.ListIssuesByProductIdApi.as_view(), ['GET'])]
for url, view, methods in api_urls:
    issue_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/issue', service.CreateIssueService.as_view(), ['POST']),
                ('/issue/<issue_id>/user/<user_id>/vote',
                 service.IssueVoteService.as_view(), ['PUT']),
                ('/issue/<issue_id>/statistics',
                 service.GetStatisticsByIssueIdService.as_view(), ['GET']),
                ('/issue/product/<product_id>',
                 service.ListIssuesByProductIdService.as_view(), ['GET'])]
issue_service_blueprint = Blueprint('issue_service', url_prefix='/service/v1')
for url, view, methods in service_urls:
    issue_service_blueprint.add_route(view, url, methods=methods)
