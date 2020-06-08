"""
路由 http 请求
"""
from sanic.blueprints import Blueprint

from app import app
from libs.jwt import jwt_wrapper
from product import api, service

###############################
# api
###############################
product_api_blueprint = Blueprint('product_api', version='1')

api_urls = [('/product',
             jwt_wrapper(api.CreateProductApi.as_view(),
                         role_ids=(app.config.ROLE_MANAGER, )), ['POST']),
            ('/products', api.ListProductsApi.as_view(), ['GET']),
            ('/product/manager/<manager_id>',
             jwt_wrapper(api.ListProductByManagerIdApi.as_view(),
                         role_ids=(app.config.ROLE_MANAGER, )), ['GET']),
            ('/product/<product_id>',
             jwt_wrapper(api.UpdateProductByIdApi.as_view(),
                         role_ids=(app.config.ROLE_MANAGER, )), ['PUT']),
            ('/product/<product_id>',
             jwt_wrapper(api.DeleteProductByIdApi.as_view(),
                         role_ids=(app.config.ROLE_MANAGER, )), ['DELETE'])]
for url, view, methods in api_urls:
    product_api_blueprint.add_route(view, url, methods=methods)

##########################
# 内部服务使用的 api
##########################
service_urls = [('/product', service.CreateProductService.as_view(), ['POST']),
                ('/products', service.ListProductsService.as_view(), ['GET']),
                ('/product/manager/<manager_id>',
                 service.ListProductByManagerService.as_view(), ['GET']),
                ('/product/<product_id>',
                 service.UpdateProductByIdService.as_view(), ['PUT']),
                ('/product/<product_id>',
                 service.DeleteProductByIdService.as_view(), ['DELETE'])]
product_service_blueprint = Blueprint('product_service',
                                      url_prefix='/service/v1')
for url, view, methods in service_urls:
    product_service_blueprint.add_route(view, url, methods=methods)
