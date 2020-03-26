import logging
from inspect import isawaitable

from marshmallow.exceptions import ValidationError

from libs.sanic_api.exceptions import APIException, InvalidJSON
from sanic.exceptions import InvalidUsage
from sanic.response import json
from sanic.views import HTTPMethodView

logger = logging.getLogger('issue_feedback')


def ok_response(body, message="", *args, **kwargs):
    """成功的 response
    """
    new_body = {'ok': True, 'message': message, 'result': body}
    return json(new_body, *args, **kwargs)


def failed_response(error_type, error_message, *args, **kwargs):
    """失败的 response
    """
    body = {'ok': False, 'error_type': error_type, 'message': error_message}
    return json(body, *args, **kwargs)


def validation_error_response(validation_error, *args, **kwargs):
    """字段验证失败的 response
    validation_error: ValidationError
    """
    errors = list()

    if validation_error.messages.get('_schema'):
        # 自定义的一些错误
        errors.append({
            'error_type': 'validation_error',
            'field': '_schema',
            'message': validation_error.messages.get('_schema')[0]
        })

    for field in validation_error.messages:
        field_error = {
            'error_type': 'validation_error',
            'field': field,
            'message': validation_error.messages[field][0]
        }
        errors.append(field_error)

    new_body = {'ok': False, 'errors': errors}
    return json(new_body, *args, **kwargs)


class APIBaseView(HTTPMethodView):
    """扩展 class based view, 增加异常处理
    """
    def parse_json(self, request):
        """解析 request body 为 json
        """
        # 如果使用 jwt 传递数据, 则不再解析 request body
        jwt_payload = request.get('jwt_payload')
        if jwt_payload:
            return jwt_payload

        try:
            return request.json or {}
        except InvalidUsage:
            raise InvalidJSON

    async def dispatch_request(self, request, *args, **kwargs):
        """扩展 http 请求的分发, 添加错误处理
        """
        self.request = request

        try:
            response = super(APIBaseView,
                             self).dispatch_request(request, *args, **kwargs)
            if isawaitable(response):
                response = await response
        except Exception as exception:
            response = await self.handle_exception(exception)

        return response

    async def handle_exception(self, exception):
        """处理异常
        ValidationError, APIException: 返回适当的错误信息
        else: 重新抛出异常
        """
        if isinstance(exception, ValidationError):
            response = validation_error_response(exception)
        elif isinstance(exception, APIException):
            response = failed_response(error_type=exception.error_type,
                                       error_message=exception.error_message)
        else:
            logger.error(str(exception))
            raise exception
        return response


class GetView(APIBaseView):
    """GET api view
    1. 获取数据对象
    2. 序列化数据
    """
    args_deserializer_class = None
    get_serializer_class = None

    async def get(self, request, *args, **kwargs):
        """处理 GET 请求
        """
        self.validated_data = self.get_validated_data(request, kwargs)
        target_object = await self.get_object()
        serialized_data = await self.serialize(target_object)
        return ok_response(serialized_data)

    def get_validated_data(self, request, kwargs):
        # 反序列化请求数据
        if not self.args_deserializer_class:
            return {}

        request_data = self.parse_json(request)
        # 处理 GET 参数的格式，让 marshmallow 比较容易处理
        for key, value in request.args.items():
            if isinstance(value, list) and len(value) == 1:
                request_data[key] = value[0]
            else:
                request_data[key] = value
        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def serialize(self, target_object):
        """序列化目标对象
        """
        if not self.get_serializer_class:
            return {}
        data = self.get_serializer_class().dump(target_object)
        return data

    async def get_object(self):
        """获取需要序列化的对象
        """
        raise NotImplementedError


class PutView(APIBaseView):
    """更新已知资源 view
    1. 获取上下文: 通过数据库或其他 model 层获取数据
    2. 验证请求数据
    3. 保存数据
    """
    args_deserializer_class = None
    put_serializer_class = None

    async def put(self, request, *args, **kwargs):
        self.validated_data = self.get_validated_data(request, kwargs)

        # 保存数据
        patched_object = await self.save()
        return self.response(patched_object)

    def get_validated_data(self, request, kwargs):
        # 反序列化请求数据
        if not self.args_deserializer_class:
            return {}

        request_data = self.parse_json(request)
        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def save(self):
        """根据 self.validated_data 和 self.context 保存数据到数据库
        """
        raise NotImplementedError

    def response(self, saved_object):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        if self.put_serializer_class:
            data = self.put_serializer_class().dump(saved_object)
            return ok_response(data)
        else:
            return ok_response({})


class PatchView(APIBaseView):
    """局部更新资源 view
    1. 获取上下文: 通过数据库或其他 model 层获取数据
    2. 验证请求数据
    3. 保存数据
    """
    args_deserializer_class = None
    patched_serializer_class = None

    async def patch(self, request, *args, **kwargs):
        self.validated_data = self.get_validated_data(request, kwargs)

        # 保存数据
        patched_object = await self.save()
        return self.response(patched_object)

    def get_validated_data(self, request, kwargs):
        # 反序列化请求数据
        if not self.args_deserializer_class:
            return {}

        request_data = self.parse_json(request)
        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def save(self):
        """根据 self.validated_data 和 self.context 保存数据到数据库
        """
        raise NotImplementedError

    def response(self, saved_object):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        if self.patched_serializer_class:
            data = self.patched_serializer_class().dump(saved_object)
            return ok_response(data)
        else:
            return ok_response({})


class PostView(APIBaseView):
    """创建数据的 view
    """
    args_deserializer_class = None
    post_serializer_class = None

    async def post(self, request, *args, **kwargs):
        self.validated_data = self.get_validated_data(request, kwargs)

        # 保存数据
        saved_object = await self.save()
        return await self.response(saved_object)

    def get_validated_data(self, request, kwargs):
        # 反序列化请求数据
        if not self.args_deserializer_class:
            return {}

        request_data = self.parse_json(request)
        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def save(self):
        """根据 self.validated_data 和 self.context 保存数据到数据库
        """
        raise NotImplementedError

    async def response(self, saved_object):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        if self.post_serializer_class:
            data = self.post_serializer_class().dump(saved_object)
            return ok_response(data)
        else:
            return ok_response({})


class DeleteView(APIBaseView):
    """删除数据的 view
    1. 获取上下文: 通过数据库或其他 model 层获取数据
    2. 验证请求数据
    3. 保存数据
    """
    args_deserializer_class = None

    async def delete(self, request, *args, **kwargs):
        self.validated_data = self.get_validated_data(request, kwargs)

        # 保存数据
        deleted_object = await self.save()
        return self.response(deleted_object)

    def get_validated_data(self, request, kwargs):
        # 反序列化请求数据
        if not self.args_deserializer_class:
            return {}

        request_data = self.parse_json(request)
        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def save(self):
        """
        具体执行操作, 由子类实现
        """
        raise NotImplementedError

    def response(self, deleted_object):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        return ok_response({})


class ListView(APIBaseView):
    """List api view
    1. 反序列化传入的参数
    2. 获取一组数据
    3. 序列化一组数据
    """
    # 传入参数的的反序列化器
    args_deserializer_class = None
    # 过滤出来的结果的序列化器
    list_serializer_class = None
    list_result_name = 'items'

    async def get(self, request, *args, **kwargs):
        """处理 GET 请求
        """
        self.validated_data = self.get_validated_data(request, kwargs)
        target_objects = await self.filter_objects()
        return self.response(target_objects)

    def get_validated_data(self, request, kwargs):
        if not self.args_deserializer_class:
            return {}

        request_data = {}
        # 处理 GET 参数的格式，让 marshmallow 比较容易处理
        for key, value in request.args.items():
            if isinstance(value, list) and len(value) == 1:
                request_data[key] = value[0]
            else:
                request_data[key] = value

        request_data.update(kwargs)
        deserializer = self.args_deserializer_class()
        validated_data = deserializer.load(request_data)
        return validated_data

    async def filter_objects(self):
        """获取需要序列化的对象
        """
        raise NotImplementedError

    def response(self, results):
        """响应结果
        默认返回空 json 对象, 需要修改则在子类中覆盖这个方法
        """
        if not self.list_serializer_class:
            return ok_response({})

        _serializer = self.list_serializer_class()
        return ok_response({
            self.list_result_name:
            _serializer.dump(results, many=True),
        })


class AdminListView(GetView):
    """管理界面用的ListView
    """
    async def get(self, request, *args, **kwargs):
        """处理 GET 请求
        """
        self.validated_data = self.get_validated_data(request, kwargs)
        target_object = await self.get_object(request, kwargs)
        serialized_data = await self.serialize(target_object)
        return ok_response(serialized_data)

    async def get_context(self, request, kwargs):
        return {
            'start': int(request.args.get('start', 0)),
            'end': int(request.args.get('end', 10)),
            'order': request.args.get('order', 'desc'),
            'sort': request.args.get('sort', 'created_at'),
            'keyword': request.args.get('keyword', None),
            'size': int(request.args.get('size', 10)),
            'paging_state': request.args.get('paging_state', None),
        }

    async def get_all_objects(self):
        raise NotImplementedError

    def search(self, results):
        raise NotImplementedError

    def paging_results(self, results, start, end, order_by, sort_field):
        if order_by.lower() == 'desc':
            reverse = True
        else:
            reverse = False

        sorted_results = sorted(results,
                                key=lambda x: getattr(x, sort_field),
                                reverse=reverse)
        return sorted_results[start:end], len(sorted_results)

    async def get_object(self, request, kwargs):
        self.context = await self.get_context(request, kwargs)

        results = await self.get_all_objects()
        results = self.search(results)

        paging_results, total_results = self.paging_results(
            results, self.context['start'], self.context['end'],
            self.context['order'], self.context['sort'])
        self.context['total'] = total_results
        return paging_results

    async def serialize(self, results):
        _serializer = self.get_serializer_class()
        return {
            'items': _serializer.dump(results, many=True),
            'total': self.context['total']
        }
