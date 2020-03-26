"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from example import admin, api, service

###############################
# api
###############################
api_blueprint = Blueprint('api', version='1')

api_urls = [
    ('/example', api.ExampleView.as_view(), ['POST']),
]
for url, view, methods in api_urls:
    api_blueprint.add_route(view, url, methods=methods)

###############################
# Admin 接口
###############################
admin_blueprint = Blueprint('admin')

admin_blueprint.add_route(admin.ListExampleView.as_view(),
                          '/admin/example',
                          methods=['GET'])

##########################
# 内部服务使用的 api
##########################
service_urls = [
    ('/example/<example_field>', service.GetExampleView.as_view(), ['GET']),
]
service_blueprint = Blueprint('service', url_prefix='/service/v1')
for url, view, methods in service_urls:
    service_blueprint.add_route(view, url, methods=methods)
