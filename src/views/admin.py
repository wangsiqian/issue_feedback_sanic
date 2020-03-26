from libs.sanic_api.views import AdminListView
from models.db_schema import Example
from views.serializers import ExampleSerializer


class ListExampleView(AdminListView):
    get_serializer_class = ExampleSerializer

    async def get_all_objects(self):
        results, paging_state = await Example.async_fetch(
            fields=['id', 'created_at'],
            fetch_size=self.context['size'],
            paging_state=self.context['paging_state'])
        self.context['new_paging_state'] = paging_state
        return results

    def search(self, results):
        return results
