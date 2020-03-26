import importlib
import time

import pytest
from cassandra.cluster import NoHostAvailable
from sanic.server import HttpProtocol
from tests.docs import DocsGenerator

from configs.loader import get_config_from_env
from libs.sanic_api.models.management import DatabaseManagement

# 当前单元测试的序号, 用于防止名字相同的单元测试创建出相同的 keyspace
keyspace_num = 0


@pytest.fixture
def app(request):
    """创建 sanic app, 进入时同步数据表, 退出时删除测试数据
    """
    global keyspace_num

    from app.server import sync_db, app as sanic_app

    # 发现没有加载 config 时, 从环境变量中加载 config
    if 'CASSANDRA_NODES' not in sanic_app.config:
        config_object = importlib.import_module(get_config_from_env())
        sanic_app.config.from_object(config_object)

    db_management = DatabaseManagement(sanic_app, timeout=60)
    # 防止运行 CI 时连接失败, 等待 Cassandra 启动重新同步一次
    try:
        sync_db()
    except NoHostAvailable:
        time.sleep(20)
        sync_db()

    yield sanic_app
    db_management.drop_db()


@pytest.fixture
def client(loop, app, sanic_client, docs_generator):
    """创建 http client
    """
    _client = loop.run_until_complete(sanic_client(app, protocol=HttpProtocol))
    _client.docs_generator = docs_generator

    return _client


@pytest.fixture(scope='session', autouse=True)
def docs_generator():
    """设置 scope 为 session, 在整个测试中只运行一次
    """
    generator = DocsGenerator()
    yield generator
    generator.build_docs()
