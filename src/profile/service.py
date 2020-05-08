from profile.exceptions import ProfileAlreadyExist
from profile.models.profile import Profile
from profile.models.serializers import ProfileSerializer

from libs.sanic_api.views import PostView


class CreateProfileService(PostView):
    """创建用户资料
    """
    args_deserializer_class = ProfileSerializer
    post_serializer_class = ProfileSerializer

    async def save(self):
        user_id = self.validated_data['user_id']
        try:
            await Profile.async_get(user_id=user_id)
        except Profile.DoesNotExist:
            return await Profile.new(user_id=user_id,
                                     nickname=self.validated_data['nickname'],
                                     gender=self.validated_data['gender'])

        raise ProfileAlreadyExist
