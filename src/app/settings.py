from profile import profile, profile_api_blueprint, profile_service_blueprint

from account import account, account_api_blueprint, account_service_blueprint
from issue import issue, issue_api_blueprint, issue_service_blueprint
from product import product, product_api_blueprint, product_service_blueprint

# 蓝图（添加新的 app 需要到这里添加蓝图）
blueprints = [
    # profile
    profile_api_blueprint,
    profile_service_blueprint,
    # product
    product_api_blueprint,
    product_service_blueprint,
    # account
    account_api_blueprint,
    account_service_blueprint,
    # issue
    issue_api_blueprint,
    issue_service_blueprint
]

# models
models = [account, profile, product, issue]
