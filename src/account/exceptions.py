from libs.sanic_api.exceptions import APIException


class PasswordIllegal(APIException):
    error_type = 'password_illegal'
    error_message = '账号需至少有一个大写字母、一个小写字母、包含符号.~!@&%#_，且长度为8～16'


class AccountAlreadyExist(APIException):
    error_type = 'account_already_exist'
    error_message = '该账号已经存在，请登录'


class AccountNotFound(APIException):
    error_type = 'account_not_found'
    error_message = '账号不存在，请创建'


class PasswordWrong(APIException):
    error_type = 'password_wrong'
    error_message = '密码错误'
