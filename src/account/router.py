"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from account import api, service

###############################
# api
###############################
account_api_blueprint = Blueprint('account_api', version='1')

api_urls = [
    ('/account', api.CreateAccountApi.as_view(), ['POST']),
]
for url, view, methods in api_urls:
    account_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [
    ('/account', service.CreateAccountService.as_view(), ['POST']),
]
account_service_blueprint = Blueprint('account_service',
                                      url_prefix='/service/v1')
for url, view, methods in service_urls:
    account_service_blueprint.add_route(view, url, methods=methods)
