"""
sanic server
"""

from profile import profile_api_blueprint, profile_service_blueprint

from account import account_api_blueprint, account_service_blueprint
from app import app

app.blueprint(account_api_blueprint)
app.blueprint(account_service_blueprint)
app.blueprint(profile_service_blueprint)
app.blueprint(profile_api_blueprint)


def sync_db():
    """同步数据库, 添加了新的 model 需要加入到这个函数中
    """
    import os
    from libs.sanic_api.models.management import DatabaseManagement
    from account import account
    from profile import profile

    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'
    DatabaseManagement(app, timeout=60).sync_db(account, profile)


def run_server():
    """启动服务器
    根据启动参数加载配置, 如果没有相应的配置文件直接抛出错误
    """
    app.run(host=app.config.HOST,
            port=app.config.PORT,
            workers=app.config.WORKERS,
            debug=app.config.DEBUG)
