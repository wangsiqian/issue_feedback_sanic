"""
路由 http 请求
"""
from profile import api, service

from sanic.blueprints import Blueprint

###############################
# api
###############################
profile_api_blueprint = Blueprint('profile_api', version='1')

api_urls = [('/profile', api.CreateProfileApi.as_view(), ['POST']),
            ('/profile/<user_id>', api.GetProfileByIdService.as_view(),
             ['GET'])]
for url, view, methods in api_urls:
    profile_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/profile', service.CreateProfileService.as_view(), ['POST']),
                ('/profile/<user_id>', service.GetProfileByIdService.as_view(),
                 ['GET'])]
profile_service_blueprint = Blueprint('profile_service',
                                      url_prefix='/service/v1')
for url, view, methods in service_urls:
    profile_service_blueprint.add_route(view, url, methods=methods)
