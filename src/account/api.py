from account.service import CreateAccountService, LoginService


class CreateAccountApi(CreateAccountService):
    post_serializer_class = None


class LoginApi(LoginService):
    pass
