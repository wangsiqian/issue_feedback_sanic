from app import app
from example.models.serializers import ExampleSerializer
from libs.sanic_api.views import GetView


class GetExampleView(GetView):
    """获取所有记录
    """

    args_deserializer_class = ExampleSerializer

    async def get_object(self):
        return await app.cassandra.execute_future("""SELECT * FROM example
            """)

    async def serialize(self, objects):
        """序列化
        """
        serialized_data = ExampleSerializer().dump(objects, many=True)
        return serialized_data
