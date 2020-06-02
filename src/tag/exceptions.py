from libs.sanic_api.exceptions import APIException


class TagAlreadyExist(APIException):
    error_type = 'tag_already_exist'
    error_message = '该标签已经存在了'
