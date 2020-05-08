import logging

from aio_pika import connect_robust
from sanic import Sanic

logger = logging.getLogger('sanic')

rabbitmq_connection = None


async def setup_rabbitmq_connection_listener(app, loop):
    global rabbitmq_connection

    rabbitmq_connection = await connect_robust(
        host=app.config.RABBITMQ_HOSTNAME,
        port=app.config.RABBITMQ_PORT,
        loop=loop)
    channel = await rabbitmq_connection.channel()

    exchange = await channel.declare_exchange(app.config.RABBITMQ_EXCHANGE)
    queue = await channel.declare_queue(app.config.RABBITMQ_QUEUE)
    await queue.bind(exchange, app.config.RABBITMQ_ROUTING_KEY)

    app.exchange = exchange


async def teardown_rabbitmq_connection_listener(app, loop):
    global rabbitmq_connection
    if rabbitmq_connection:
        await rabbitmq_connection.close()


def register_rabbitmq(app: Sanic):
    app.listener('before_server_start')(setup_rabbitmq_connection_listener)
    app.listener('after_server_stop')(teardown_rabbitmq_connection_listener)
