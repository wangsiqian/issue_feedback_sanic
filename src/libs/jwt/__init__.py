from datetime import datetime, timedelta

import jwt
from sanic.request import Request

from app import app
from libs.sanic_api.views import failed_response

config = app.config


async def generate_token(exp, **kwargs):
    kwargs.update({'exp': datetime.utcnow() + timedelta(seconds=exp)})
    token = jwt.encode(payload=kwargs, key=config.JWT_SECRET)

    return token.decode('utf-8')


def decode_token(token):
    try:
        payload = jwt.decode(token,
                             key=config.JWT_SECRET,
                             algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # jwt 默认使用 payload 中的 exp 字段来验证是否过期, 类型是 timestamp
        return failed_response(error_message='此请求已过期',
                               error_type='api_signature_expired')

    # 验证过期后删除无用字段
    payload.pop('exp', None)

    return payload


async def jwt_middleware(request: Request, required: bool, role_ids):
    """中间件, 验证 jwt 并解析 jwt payload 转换为 request.payload
    """
    raw_jwt = request.headers.get('Authorization', None)
    if not raw_jwt:
        return failed_response(error_message='此 API 签名不正确',
                               error_type='api_signature_invalid')

    payload = decode_token(raw_jwt)
    if not required and not role_ids:
        # 无身份的 token，解析成功则不验证
        return None

    role_id = payload.get('role_id')
    authenticate = True
    # 验证身份
    if required:
        if role_id not in config.ROLES:
            authenticate = False
    else:
        if role_id not in role_ids:
            authenticate = False

    if not authenticate:
        return failed_response(error_message='没有权限',
                               error_type='permission_denied')


def jwt_wrapper(view, required=False, role_ids=()):
    """sanic 的 middleware 是全局的, 这个函数方便局部使用
    使用方法:
    blueprint.add_route(jwt_wrapper(CreateView.as_view()),
                        '/jwt_example',
                        methods=['POST'])

    :param required: True 为接受任何合法身份的 token
    :param role_ids: 指定合法身份
    """
    async def inner(request, *args, **kwargs):
        response = await jwt_middleware(request, required, role_ids)
        if not response:
            return await view(request, *args, **kwargs)
        else:
            return response

    return inner
