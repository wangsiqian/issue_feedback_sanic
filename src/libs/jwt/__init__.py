import jwt

from libs.sanic_api.views import failed_response
from sanic.request import Request


async def jwt_middleware(request: Request):
    """中间件, 验证 jwt 并解析 jwt payload 转换为 request.payload
    """
    raw_jwt = request.headers.get('Payload', None)
    if not raw_jwt:
        return failed_response(error_message='此 API 签名不正确',
                               error_type='api_signature_invalid')

    jwt_secret = request.app.config.JWT_SECRET
    try:
        payload = jwt.decode(raw_jwt, key=jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # jwt 默认使用 payload 中的 exp 字段来验证是否过期, 类型是 timestamp
        return failed_response(error_message='此请求已过期',
                               error_type='api_signature_expired')
    # 验证过期后删除无用字段
    payload.pop('exp', None)

    request['jwt_payload'] = payload


def jwt_wrapper(view):
    """sanic 的 middleware 是全局的, 这个函数方便局部使用
    使用方法:
    blueprint.add_route(jwt_wrapper(CreateView.as_view()),
                        '/jwt_example',
                        methods=['POST'])
    """
    async def inner(request, *args, **kwargs):
        response = await jwt_middleware(request)
        if not response:
            return await view(request, *args, **kwargs)
        else:
            return response

    return inner
