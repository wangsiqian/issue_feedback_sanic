from profile.service import (CreateProfileService, GetProfileByIdService,
                             UpdateProfileService)


class CreateProfileApi(CreateProfileService):
    post_serializer_class = None


class GetProfileByIdApi(GetProfileByIdService):
    pass


class UpdateProfileApi(UpdateProfileService):
    put_serializer_class = None
