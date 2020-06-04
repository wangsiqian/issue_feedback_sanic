from configs import *

STAGE = 'local'

# sanic server config
HOST = '127.0.0.1'
PORT = 8923
WORKERS = 4

# cassandra config
CASSANDRA_NODES = ['127.0.0.1']

assert CASSANDRA_KEYSPACE != 'sanic_template_example'

# rabbitmq
RABBITMQ_HOSTNAME = '127.0.0.1'
RABBITMQ_PORT = 5672
RABBITMQ_EXCHANGE = 'issue_feedback'
RABBITMQ_QUEUE = 'issue_feedback'
RABBITMQ_ROUTING_KEY = 'issue_feedback'
