from random import randint

import requests
import ujson
from pika import BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError
from retry import retry

from configs.loader import load_config

config = load_config()


def callback(channel, method, properties, body):
    message = ujson.loads(body)
    user_id = message.get('user_id')
    event = message.get('event')
    if not user_id or not event != 'create_profile':
        return

    response = requests.post(url='http://0.0.0.0:8000/v1/profile',
                             body={
                                 'nickname':
                                 'user' + str(randint(0, 999999)).zfill(6),
                                 'user_id':
                                 user_id
                             },
                             timeout=5)

    if response.status_code == 200:
        payload = response.json()
        print(payload)


@retry(exceptions=AMQPConnectionError, delay=5, jitter=(1, 3))
def consume():
    connection = BlockingConnection(parameters=(ConnectionParameters(
        host=config.RABBITMQ_HOSTNAME, connection_attempts=5, retry_delay=1)))

    channel = connection.channel()
    channel.queue_declare(queue=config.RABBITMQ_QUEUE)
    channel.basic_consume(queue=config.RABBITMQ_QUEUE,
                          on_message_callback=callback,
                          auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    consume()
