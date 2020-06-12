from libs.sanic_api.views import ListView, PostView
from tag.exceptions import TagAlreadyExist
from tag.models.serializers import (CreateTagSerializer,
                                    MultiCreateTagsSerializer, TagSerializer)
from tag.models.tag import Tag


class CreateTagService(PostView):
    """创建评论
    """
    args_deserializer_class = CreateTagSerializer
    post_serializer_class = TagSerializer

    async def save(self):
        name = self.validated_data['name']
        try:
            await Tag.async_get(name=name)
        except Tag.DoesNotExist:
            return await Tag.new(
                name=name,
                description=self.validated_data['description'],
                color=self.validated_data['color'])

        raise TagAlreadyExist


class ListTagsService(ListView):
    """列出评论
    """
    list_result_name = 'tags'
    args_deserializer_class = None
    list_serializer_class = TagSerializer

    async def filter_objects(self):
        tags = await Tag.async_all()
        return sorted(tags, key=lambda tag: tag.name)


class MultiCreateTagsService(PostView):
    """创建多个标签
    """
    args_deserializer_class = MultiCreateTagsSerializer
    post_serializer_class = None

    async def save(self):
        for tag in self.validated_data['tags']:
            name = tag.get('name')
            try:
                await Tag.async_get(name=name)
            except Tag.DoesNotExist:
                await Tag.new(name=name,
                              description=tag['description'],
                              color=tag['color'])
