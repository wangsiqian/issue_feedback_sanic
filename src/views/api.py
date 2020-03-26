import uuid
from datetime import datetime, timezone

from app import app
from libs.sanic_api.views import PostView
from views.serializers import ExampleSerializer


class ExampleView(PostView):
    # Fixme: 删掉 example

    args_deserializer_class = ExampleSerializer
    post_serializer_class = ExampleSerializer

    async def save(self):
        """保存数据
        """
        await app.cassandra.execute_future(
            f"""
            INSERT INTO example
            (id, example_field, created_at)
            VALUES (%s, %s, %s)
            """, (uuid.uuid4(), self.validated_data['example_field'],
                  datetime.now(timezone.utc)))

        return {'example_field': self.validated_data['example_field']}
