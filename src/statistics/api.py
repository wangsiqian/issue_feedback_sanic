from statistics.service import (CountIssueByDeveloperService,
                                CountIssueByManagerService,
                                CountIssueByUserService)


class CountIssueByUserApi(CountIssueByUserService):
    pass


class CountIssueByDeveloperApi(CountIssueByDeveloperService):
    pass


class CountIssueByManagerApi(CountIssueByManagerService):
    pass
