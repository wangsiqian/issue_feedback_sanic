from profile.service import CreateProfileService, GetProfileByIdService


class CreateProfileApi(CreateProfileService):
    post_serializer_class = None


class GetProfileByIdApi(GetProfileByIdService):
    pass
