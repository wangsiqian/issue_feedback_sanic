import logging

from aiocassandra import aiosession
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from sanic import Sanic

logger = logging.getLogger('sanic')

cassandra_cluster = None


def setup_cassandra_session_listener(app, loop):
    global cassandra_cluster

    cassandra_cluster = Cluster(app.config.CASSANDRA_NODES)
    session = cassandra_cluster.connect(app.config.CASSANDRA_KEYSPACE)
    aiosession(session)
    session.default_consistency_level = ConsistencyLevel.LOCAL_QUORUM
    app.cassandra = session


def teardown_cassandra_session_listener(app, loop):
    global cassandra_cluster
    cassandra_cluster.shutdown()


def register_cassandra(app: Sanic):
    app.listener('before_server_start')(setup_cassandra_session_listener)
    app.listener('after_server_stop')(teardown_cassandra_session_listener)
