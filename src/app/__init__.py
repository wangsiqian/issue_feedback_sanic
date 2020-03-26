"""
初始化 sanic app
"""
from sanic import Sanic

from libs.cassandra.db_session import register_cassandra
from libs.sanic_api.models import register_cassandra_session

app = Sanic()

# 注册组件, 不需要的组件可以不注册; 注册的组件在 app.run() 后才会启动
register_cassandra_session(app)
register_cassandra(app)
