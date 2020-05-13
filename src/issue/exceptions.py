from libs.sanic_api.exceptions import APIException


class IssueAlreadyExist(APIException):
    error_type = 'issue_already_exist'
    error_message = '您已经反馈过相关问题了'
