from libs.sanic_api.exceptions import APIException


class ProfileAlreadyExist(APIException):
    error_type = 'profile_already_exist'
    error_message = '用户资料已经存在'
