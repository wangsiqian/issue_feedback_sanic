from random import randint

import ujson
from aio_pika import Message
from jwt import PyJWTError

from account.exceptions import (AccountAlreadyExist, AccountNotFound,
                                CodeAlreadyExpired, CodeAlreadySent,
                                PasswordWrong)
from account.models.account import Account, CodeRecord
from account.models.serializers import (AccountIdSerializer,
                                        CreateAccountServiceSerializer,
                                        LoginSerializer, RoleIdSerializer,
                                        SessionSerializer, UserIdSerializer,
                                        ValidationSerializer)
from app import app
from libs.jwt import decode_token, generate_token
from libs.sanic_api.views import GetView, PostView


class CreateAccountService(PostView):
    """创建账号
    """
    args_deserializer_class = CreateAccountServiceSerializer

    async def save(self):
        try:
            # 解析 token
            token_payload = decode_token(self.validated_data['validate_token'])
        except PyJWTError:
            raise CodeAlreadyExpired
        else:
            if not isinstance(token_payload, dict):
                # 可能解析失败为其他对象
                raise CodeAlreadyExpired

        account_id = self.validated_data['account_id']
        validate_code = self.validated_data['validate_code']
        if account_id != token_payload.get(
                'account_id') or validate_code != token_payload.get(
                    'validate_code'):
            # 验证身份
            raise CodeAlreadyExpired

        try:
            await Account.async_get(account_id=account_id)
        except Account.DoesNotExist:
            return await Account.new(account_id=account_id,
                                     role_id=self.validated_data['role_id'],
                                     password=self.validated_data['password'])

        raise AccountAlreadyExist


class SendCodeService(PostView):
    """发送验证码
    """
    args_deserializer_class = AccountIdSerializer
    post_serializer_class = ValidationSerializer

    async def save(self):
        account_id = self.validated_data['account_id']
        try:
            await CodeRecord.async_get(account_id=account_id)
        except CodeRecord.DoesNotExist:
            # 发送记录
            await CodeRecord.new(account_id=account_id)

            # 生成验证码
            validate_code = str(randint(0, 999999)).zfill(6)
            validate_token = await generate_token(exp=app.config.JWT_CODE_EXP,
                                                  account_id=account_id,
                                                  validate_code=validate_code)

            await app.exchange.publish(
                Message(ujson.dumps({
                    'account_id': account_id,
                    'validate_code': validate_code,
                    'event': 'send_code'
                }).encode(),
                        content_type='application/json'),
                app.config.RABBITMQ_ROUTING_KEY)

            return {
                'validate_token': validate_token,
                'validate_code': validate_code
            }

        raise CodeAlreadySent


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

        token = await generate_token(exp=app.config.JWT_SESSION_EXP,
                                     user_id=str(account.user_id),
                                     role_id=account.role_id),

        return {
            'token': token[0],
            'user_id': account.user_id,
            'role_id': account.role_id
        }


class GetRoleIdService(GetView):
    args_deserializer_class = UserIdSerializer
    get_serializer_class = RoleIdSerializer

    async def get_object(self):
        try:
            return await Account.async_get(
                user_id=self.validated_data['user_id'])
        except Account.DoesNotExist:
            raise AccountNotFound
