"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from app import app
from tag import api, service

###############################
# api
###############################

config = app.config

tag_api_blueprint = Blueprint('tag_api', version='1')

api_urls = [('/tags', api.ListTagsApi.as_view(), ['GET'])]
for url, view, methods in api_urls:
    tag_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/tag', service.CreateTagService.as_view(), ['POST']),
                ('/tags', service.MultiCreateTagsService.as_view(), ['POST']),
                ('/tags', service.ListTagsService.as_view(), ['GET'])]
tag_service_blueprint = Blueprint('tag_service', url_prefix='/service/v1')
for url, view, methods in service_urls:
    tag_service_blueprint.add_route(view, url, methods=methods)
