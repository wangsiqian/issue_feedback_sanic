from profile.service import (CreateProfileService, GetProfileByIdService,
                             UpdateProfileService)

from libs.sanic_api.exceptions import PermissionDenied


class CreateProfileApi(CreateProfileService):
    post_serializer_class = None


class GetProfileByIdApi(GetProfileByIdService):
    pass


class UpdateProfileApi(UpdateProfileService):
    put_serializer_class = None

    async def save(self):
        if self.validated_data['user_id'] != self.token_user_id:
            raise PermissionDenied

        return await super().save()
