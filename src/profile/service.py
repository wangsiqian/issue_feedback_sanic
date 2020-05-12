from profile.exceptions import ProfileAlreadyExist, ProfileNotFound
from profile.models.profile import Profile
from profile.models.serializers import (CreateProfileSerializer,
                                        ProfileSerializer, UserIdSerializer)

from libs.sanic_api.views import GetView, PostView


class CreateProfileService(PostView):
    """创建用户资料
    """
    args_deserializer_class = CreateProfileSerializer
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


class GetProfileByIdService(GetView):
    """通过用户ID查找用户资料
    """
    args_deserializer_class = UserIdSerializer
    get_serializer_class = ProfileSerializer

    async def get_object(self):
        try:
            profile = await Profile.async_get(
                user_id=self.validated_data['user_id'])
        except Profile.DoesNotExist:
            raise ProfileNotFound

        return profile
