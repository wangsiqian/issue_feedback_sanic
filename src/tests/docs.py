import json
import os

import pytest
from pytest_sanic.utils import TestClient

import decorator


def get_parent_dir(path, depth):
    if depth == 1:
        return os.path.abspath(os.path.join(path, os.pardir))

    return get_parent_dir(get_parent_dir(path, depth - 1), 1)


class Api:
    title = None
    path = None
    method = None
    headers = {}
    params = {}
    body = {}
    responses = {}

    def __init__(self, title, path, method, headers, params, body, responses):
        self.title = title
        self.path = path
        self.method = method
        if headers:
            self.headers = headers
        if params:
            self.params = params
        if body:
            self.body = body
        self.responses = responses


class DocsGenerator:
    """用于在跑测试时 创建生成 API 文档

    docs = Docs()
    docs.add_api_docs(...)
    docs.add_api_docs(...)
    docs.build()
    """
    apis = dict()

    def add_api_docs(self,
                     title,
                     path,
                     method,
                     headers,
                     params,
                     body,
                     responses,
                     file=None):
        if file is None:
            file = 'readme.md'
        if file not in self.apis:
            self.apis[file] = list()
        self.apis[file].append(
            Api(title, path, method, headers, params, body, responses))

    def build_docs(self):
        # 生成目录
        toc = ''
        for file in self.apis:
            toc += f'[{file}]({file})\n'

        docs_dir = os.path.join(get_parent_dir(os.path.abspath(__file__), 3),
                                'docs/')
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)

        for file in self.apis:
            file_path = os.path.join(docs_dir + file)
            f = open(file_path, 'w+', encoding='utf-8')
            f.write(toc)
            for index, api in enumerate(self.apis[file]):
                self._build(api, f, index)
            f.close()

    def _build(self, api, f, index):
        title = '\n## {} {}\n'.format(index, api.title)
        f.write(title)

        f.write('**请求**: \n\n')
        f.write('| 方法名 | 参数 | 描述 |\n| --- | --- | --- |\n')
        f.write('| path | `{}` | - |\n'.format(api.path))
        f.write('| method | `{}` | - |\n'.format(api.method))

        for key, value in api.headers.items():
            if value:
                f.write('| header | `{}` | {} |\n'.format(key, value))

        for key, value in api.params.items():
            if value:
                f.write('| params | `{}` | {} |\n'.format(key, value))

        for key, value in api.body.items():
            if value:
                f.write('| body | `{}` | {} |\n'.format(key, value))

        f.write('\n')

        for description, response in api.responses.items():
            _response = json.dumps(response,
                                   indent=2,
                                   ensure_ascii=False,
                                   sort_keys=True)
            response = f'{description}: \n```json\n{_response}\n```\n'
            f.write(response)


@pytest.mark.docs
def api_docs(title,
             path,
             method,
             headers=None,
             params=None,
             body=None,
             file=None):
    """装饰器, 在测试函数上使用, 生成文档
    example:

    @api_docs(title='请求获取好友列表', path='/v1/friend/', method='GET',
              body=None)
    async def test_list_friends(client):
        ...
        return {'正确响应': json_result}
    """
    def wrapper(func):
        async def inner(_func, *args, **kwargs):
            """获取测试运行结果作为 http response 添加到文档中
            """
            responses = await _func(*args, **kwargs)

            client = None
            for arg in args:
                if isinstance(arg, TestClient):
                    client = arg
                    break
            if client is None:
                raise Exception('Test client not found')

            client.docs_generator.add_api_docs(title=title,
                                               path=path,
                                               method=method,
                                               headers=headers,
                                               params=params,
                                               body=body,
                                               responses=responses,
                                               file=file)
            return responses

        return decorator.decorator(inner, func)

    return wrapper
