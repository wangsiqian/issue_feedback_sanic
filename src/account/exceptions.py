from libs.sanic_api.exceptions import APIException


class PasswordIllegal(APIException):
    error_type = 'password_illegal'
    error_message = '密码不能纯数字，至少包含一个字母或一个符号.~!@&%#_，且长度为8～16'


class AccountAlreadyExist(APIException):
    error_type = 'account_already_exist'
    error_message = '该账号已经存在，请登录'


class AccountNotFound(APIException):
    error_type = 'account_not_found'
    error_message = '账号不存在，请创建'


class PasswordWrong(APIException):
    error_type = 'password_wrong'
    error_message = '密码错误'


class CodeAlreadyExpired(APIException):
    error_type = 'code_already_expired'
    error_message = '验证码已经失效'


class CodeAlreadySent(APIException):
    error_type = 'code_already_sent'
    error_message = '验证码已经发送'
