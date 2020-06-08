from libs.sanic_api.exceptions import APIException


class ProductNotFound(APIException):
    error_type = 'product_not_found'
    error_message = '未找到该产品信息'


class ProductAlreadyExist(APIException):
    error_type = 'product_already_exist'
    error_message = '产品名需要唯一'
