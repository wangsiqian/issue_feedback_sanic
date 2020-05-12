from account.exceptions import (AccountAlreadyExist, AccountNotFound,
                                PasswordWrong)
from account.models.account import Account
from account.models.serializers import (CreateAccountSerializer,
                                        LoginSerializer, SessionSerializer)
from app import app
from libs.jwt import generate_token
from libs.sanic_api.views import PostView


class CreateAccountService(PostView):
    """获取所有记录
    """
    args_deserializer_class = CreateAccountSerializer

    async def save(self):
        try:
            await Account.async_get(
                account_id=self.validated_data['account_id'])
        except Account.DoesNotExist:
            return await Account.new(
                account_id=self.validated_data['account_id'],
                role_id=self.validated_data['role_id'],
                password=self.validated_data['password'])

        raise AccountAlreadyExist


class LoginService(PostView):
    """
    用户登陆
    返回 token 和 身份
    """
    args_deserializer_class = LoginSerializer
    post_serializer_class = SessionSerializer

    async def save(self):
        try:
            account = await Account.async_get(
                account_id=self.validated_data['account_id'])
        except Account.DoesNotExist:
            raise AccountNotFound

        # 验证密码
        result = await account.verify_password(self.validated_data['password'])
        if result is False:
            raise PasswordWrong

        token = await generate_token(exp=app.config.JWT_EXP,
                                     user_id=str(account.user_id),
                                     role_id=account.role_id),

        return {
            'token': token[0],
            'user_id': account.user_id,
            'role_id': account.role_id
        }
