from account.models.serializers import (CreateAccountApiSerializer,
                                        ValidationTokenSerializer)
from account.service import (CreateAccountService, GetRoleIdService,
                             LoginService, SendCodeService, ModifyPasswordService)
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
    post_serializer_class = ValidationTokenSerializer


class GetRoleIdApi(GetRoleIdService):
    pass


class ModifyPasswordApi(ModifyPasswordService):
    post_serializer_class = None
