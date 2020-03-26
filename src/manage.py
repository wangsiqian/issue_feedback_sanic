#!/usr/bin/env python
import importlib
import os
import sys

import click
import pytest

from app import app
from configs.loader import get_config_from_env


@click.group()
@click.version_option()
@click.option('--config',
              help="""默认使用: configs.docker_compose, 所有的 config 都在 configs 目录下.
         例如:configs.your_config.
         如果没有使用 config 参数, 默认读取环境变量 STAGE 来配置 config.""")
def cli(config):
    """Sanic 项目管理工具
    """
    # 加载配置模块, 如果没有设置 config 参数, 从环境变量中读取
    if not config:
        config = get_config_from_env()

    config_object = importlib.import_module(config)
    app.config.from_object(config_object)
    click.echo('\nUsing config: %s\n' % config)


@cli.command('test')
@click.argument('test_name', required=False)
def run_test(test_name):
    """
    如果指定 test_name 可以单独运行某一个 test，不指定就运行所有测试

    执行 pytest 测试, 测试时允许 cqlengine 修改数据表结构。
    """
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 添加 -x option, 遇到 error 和 failed 直接退出
    pytest_args = [
        '--cov-report=term-missing',
        '-x',
        '-v',
        # -s 让跑测试的时候可以用 ipython
        '-s',
        os.path.join(base_dir, 'tests')
    ]
    # 测试的时候动态的使用不同的KEYSAPCE
    app.config.CASSANDRA_KEYSPACE = 'test_' + app.config.CASSANDRA_KEYSPACE
    print('数据库创建的KEYSAPCE是' + app.config.CASSANDRA_KEYSPACE)

    if test_name:
        click.echo(f'运行单个测试：{test_name}')
        pytest_args.append(f'-k {test_name}')
    else:
        click.echo('正在运行所有的测试, 使用 manage.py test foo 可以运行单个测试')

    click.echo(f'pytest {" ".join(pytest_args)}')
    sys.exit(pytest.main(pytest_args))


@cli.command('testall')
def run_all_test():
    """跑所有的测试，即使错了，也不停，会全部跑完
    """
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 添加 -x option, 遇到 error 和 failed 直接退出
    pytest_args = [
        '--cov=views',
        '--cov-report=term-missing',
        '--cov-report=annotate',
        '-x',
        '-v',
        # -s 让跑测试的时候可以用 ipython
        '-s',
        # 直到遇到100个错误的时候，才停下
        '--maxfail=100',
        os.path.join(base_dir, 'tests')
    ]
    # 测试的时候动态的使用不同的KEYSAPCE
    app.config.CASSANDRA_KEYSPACE = 'test_' + app.config.CASSANDRA_KEYSPACE
    print('数据库创建的KEYSAPCE是' + app.config.CASSANDRA_KEYSPACE)

    click.echo('正在运行所有的测试, 查询 FAILED 可以看到失败的测试')

    click.echo(f'pytest {" ".join(pytest_args)}')
    sys.exit(pytest.main(pytest_args))


@cli.command('testdoc')
def run_all_doc_test():
    """跑所有的测试，即使错了，也不停，会全部跑完
    """
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'

    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 添加 -x option, 遇到 error 和 failed 直接退出
    pytest_args = [
        '-x', '-v', '-svv', '-m "docs"',
        os.path.join(base_dir, 'tests')
    ]
    # 测试的时候动态的使用不同的KEYSAPCE
    app.config.CASSANDRA_KEYSPACE = 'test_' + app.config.CASSANDRA_KEYSPACE
    print('数据库创建的KEYSAPCE是' + app.config.CASSANDRA_KEYSPACE)

    click.echo('正在运行所有的 doc 测试')

    click.echo(f'pytest {" ".join(pytest_args)}')
    sys.exit(pytest.main(pytest_args))


@cli.command('runserver')
def runserver():
    """
    运行服务器
    """
    from app.server import run_server

    run_server()


@cli.command('sync_db')
def sync_db():
    """同步数据库
    """
    from app.server import sync_db as _sync_db
    _sync_db()


if __name__ == '__main__':
    cli()
