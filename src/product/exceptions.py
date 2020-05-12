from libs.sanic_api.exceptions import APIException


class ProductNotFound(APIException):
    error_type = 'product_not_found'
    error_message = '未找到该产品信息'
