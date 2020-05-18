from account.models.serializers import CreateAccountApiSerializer
from account.service import CreateAccountService, LoginService, SendCodeService
from app import app


class CreateAccountApi(CreateAccountService):
    args_deserializer_class = CreateAccountApiSerializer
    post_serializer_class = None

    async def save(self):
        # 默认为用户身份
        self.validated_data['role_id'] = app.config.ROLE_USER

        return await super().save()


class LoginApi(LoginService):
    pass


class SendCodeApi(SendCodeService):
    pass
