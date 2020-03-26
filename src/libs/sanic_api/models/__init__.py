import logging

from libs.sanic_api.models.management import DatabaseManagement
from sanic import Sanic

logger = logging.getLogger('sanic')


def setup_db_session_listener(app, loop):
    """make cassandra session async
    """
    db_management = DatabaseManagement(app)
    db_management.connect()
    logger.info('Cassandra session prepared')


async def teardown_db_session_listener(app, loop):
    """断开连接
    """
    db_management = DatabaseManagement(app)
    db_management.disconnect()
    logger.info('Cassandra session has shutdown')


def register_cassandra_session(app: Sanic):
    """启动 Cassandra db session
    """
    app.listener('before_server_start')(setup_db_session_listener)
    app.listener('after_server_stop')(teardown_db_session_listener)
