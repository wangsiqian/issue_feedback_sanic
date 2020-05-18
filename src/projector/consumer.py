import ujson
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError
from retry import retry

from configs.loader import load_config
from projector.handler_proxy import HandlerProxy

config = load_config()


def callback(channel, method, properties, body):
    message = ujson.loads(body)

    # 处理 message
    proxy = HandlerProxy(message)
    proxy.do_something()


@retry(exceptions=AMQPConnectionError, delay=5, jitter=(1, 3))
def consume():
    connection = BlockingConnection(parameters=(ConnectionParameters(
        host=config.RABBITMQ_HOSTNAME, connection_attempts=5, retry_delay=1)))

    channel = connection.channel()
    channel.queue_declare(queue=config.RABBITMQ_QUEUE)
    channel.basic_consume(queue=config.RABBITMQ_QUEUE,
                          on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    consume()
