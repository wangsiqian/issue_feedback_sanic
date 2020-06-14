"""
路由 http 请求
"""
from statistics import api, service

from sanic.blueprints import Blueprint

from app import app
from libs.jwt import jwt_wrapper

###############################
# api
###############################
statistics_api_blueprint = Blueprint('user_api', version='1')

api_urls = [('/statistics/user/<owner_id>',
             jwt_wrapper(api.CountIssueByUserApi.as_view(),
                         role_ids=(app.config.ROLE_USER, )), ['GET']),
            ('/statistics/developer/<developer_id>',
             jwt_wrapper(api.CountIssueByDeveloperApi.as_view(),
                         role_ids=(app.config.ROLE_DEVELOPER, )), ['GET'])]
for url, view, methods in api_urls:
    statistics_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/statistics/user/<owner_id>',
                 service.CountIssueByUserService.as_view(), ['GET']),
                ('/statistics/developer/<developer_id>',
                 service.CountIssueByDeveloperService.as_view(), ['GET'])]
statistics_service_blueprint = Blueprint('user_service',
                                         url_prefix='/service/v1')
for url, view, methods in service_urls:
    statistics_service_blueprint.add_route(view, url, methods=methods)
