from account.exceptions import AccountAlreadyExist
from account.models.account import Account
from account.models.serializers import CreateAccountSerializer
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
