"""
基础配置信息
通过 configs/__init__.py 将这个模块设置为默认的 config
"""
DEBUG = True
STAGE = 'develop'

# sanic server config
HOST = '0.0.0.0'
PORT = 8000
WORKERS = 1

# jwt secret
JWT_SECRET = 'J2dfYmXuPgtF-1KhMk01MpT3pneSAUutp5fNNT9vPrdyJN1TD9'
# 登陆 token 失效时间
JWT_SESSION_EXP = 2 * 24 * 60 * 60
# 验证码 token 过期时间
JWT_CODE_EXP = 3 * 60

# 验证码记录时间
CODE_RECORD_TTL = 3 * 60

# cassandra config
CASSANDRA_NODES = ['cassandra']
CASSANDRA_REPLICATION_FACTOR = 1

CASSANDRA_KEYSPACE = 'issue_feedback_sanic'

# rabbitmq
RABBITMQ_HOSTNAME = 'rabbitmq'
RABBITMQ_PORT = 5672
RABBITMQ_EXCHANGE = 'issue_feedback'
RABBITMQ_QUEUE = 'issue_feedback'
RABBITMQ_ROUTING_KEY = 'issue_feedback'

# role
ROLE_USER = 'USER'
ROLE_DEVELOPER = 'DEVELOPER'
ROLE_MANAGER = 'MANAGER'

# RPC hostname
CREATE_PROFILE_URL = 'http://issue_feedback_sanic:8000/v1/profile'

# email config
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
