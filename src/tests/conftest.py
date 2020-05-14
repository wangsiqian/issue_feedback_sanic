import importlib
import time
from threading import Thread

import pytest
import ujson
from cassandra.cluster import NoHostAvailable
from pika import BlockingConnection, ConnectionParameters
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


class RabbitMQConsumerThread(Thread):
    """
    帮助测试用的 rabbitmq consumer，运行在单独的线程中
    """
    def __init__(self, host, queue):
        super().__init__()

        self.connection = None
        self.channel = None

        self.messages = []
        self.create_consumer(host, queue)

    def create_consumer(self, host, queue):
        self.connection = BlockingConnection(parameters=(ConnectionParameters(
            host=host, connection_attempts=5, retry_delay=1)))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue,
                                   on_message_callback=self.callback)

    def get_one(self):
        return self.messages[-1] if self.messages else None

    def callback(self, channel, method, properties, body):
        self.messages.append(ujson.loads(body))

    def run(self):
        try:
            self.channel.start_consuming()
        except Exception as error:
            print(error)

    def stop(self):
        try:
            self.channel.stop_consuming()
        except Exception as error:
            print(error)


# @pytest.fixture()
# def rabbitmq_consumer(app):
#     """
#     scope: session, 整个 test session 中只创建一次
#     """
#     consumer = RabbitMQConsumerThread(app.config.RABBITMQ_HOSTNAME,
#                                       app.config.RABBITMQ_QUEUE)
#     consumer.start()
#     yield consumer
#     consumer.stop()
