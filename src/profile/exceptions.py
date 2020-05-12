from libs.sanic_api.exceptions import APIException


class ProfileAlreadyExist(APIException):
    error_type = 'profile_already_exist'
    error_message = '用户资料已经存在'


class ProfileNotFound(APIException):
    error_type = 'profile_not_found'
    error_message = '未找到用户资料'
