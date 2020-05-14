from libs.sanic_api.exceptions import APIException


class IssueAlreadyExist(APIException):
    error_type = 'issue_already_exist'
    error_message = '您已经反馈过相关问题了'


class StatisticsNotFount(APIException):
    error_type = 'statistics_not_found'
    error_message = '未找到该反馈的统计数据'
