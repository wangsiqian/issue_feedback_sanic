"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from app import app
from comment import api, service
###############################
# api
###############################
from libs.jwt import jwt_wrapper

config = app.config

comment_api_blueprint = Blueprint('comment_api', version='1')

api_urls = [('/comment',
             jwt_wrapper(api.CreateCommentApi.as_view(),
                         required=True), ['POST']),
            ('/comments/<issue_id>', api.CreateCommentApi.as_view(), ['GET'])]
for url, view, methods in api_urls:
    comment_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/comment', service.CreateCommentService.as_view(), ['POST']),
                ('/comments/<issue_id>',
                 service.ListCommentsByIssueIdService.as_view(), ['GET'])]
comment_service_blueprint = Blueprint('comment_service',
                                      url_prefix='/service/v1')
for url, view, methods in service_urls:
    comment_service_blueprint.add_route(view, url, methods=methods)
