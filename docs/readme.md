[readme.md](readme.md)

## 1 发送验证码
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/account/send_code` | - |
| method | `POST` | - |
| body | `account_id（必填）` | 邮箱 |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "validate_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiMTIzNDU2QHFxLmNvbSIsInZhbGlkYXRlX2NvZGUiOiI0MTkwNzEiLCJleHAiOjE1OTE1OTE4MDV9.3D21E0gkOiNlVS-Yn1H6I-5xDHjd06xOCqOw_21jlCE"
  }
}
```
权限验证错误: 
```json
{
  "error_type": "code_already_sent",
  "message": "验证码已经发送",
  "ok": false
}
```

## 2 创建帐号
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/account` | - |
| method | `POST` | - |
| body | `account_id（必填）` | 邮箱 |
| body | `password(密码)` | 密码 |
| body | `validate_token` | token |
| body | `validate_code` | 验证码 |

正确响应: 
```json
{
  "ok": true,
  "result": {}
}
```
帐号已存在: 
```json
{
  "error_type": "account_already_exist",
  "message": "该账号已经存在，请登录",
  "ok": false
}
```

## 3 登录帐号
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/login` | - |
| method | `POST` | - |
| body | `account_id（必填）` | 邮箱 |
| body | `password（必填）` | 密码 |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "role_id": "USER",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNTcxZDA0OTAtZGRkZi00YWVmLTlkMjMtMWRjZDM4N2ZiY2UxIiwicm9sZV9pZCI6IlVTRVIiLCJleHAiOjE1OTE3NjQ0MzF9.r30f9L7fKU0kIAR8zjdl0xpULsrlzZeKf-ZPuiPEVHg",
    "user_id": "571d0490-dddf-4aef-9d23-1dcd387fbce1"
  }
}
```
密码错误: 
```json
{
  "error_type": "password_wrong",
  "message": "密码错误",
  "ok": false
}
```

## 4 创建评论
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/comment` | - |
| method | `POST` | - |
| header | `Authorization` | 用户 Token |
| body | `issue_id(必填)` | 问题id |
| body | `user_id(必填)` | 用户id |
| body | `receiver_id(必填)` | 接收者id |
| body | `content(必填)` | 内容 |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "content": "不错的建议",
    "created_at": "2020-06-08T04:47:26.456119",
    "issue_id": "67badb09-7712-4df8-8d42-c3ded42c4c96",
    "receiver_id": "603fa22b-27e9-4ccc-8547-ad5634b3e811",
    "user_id": "ec84f421-4575-4f8d-991f-aa29fabc9e7e"
  }
}
```

## 5 获取评论列表
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/comments/{issue_id}` | - |
| method | `GET` | - |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "comments": [
      {
        "comment_id": "93d65e5e-65f3-439a-bff1-c6b158ec1cf7",
        "content": "不错的建议",
        "created_at": "2020-06-08T04:47:29.240000",
        "owner": {}
      },
      {
        "comment_id": "adf2ad84-79e8-4703-ae3d-72a4fc01f4ae",
        "content": "不错的建议",
        "created_at": "2020-06-08T04:47:29.267000",
        "owner": {}
      },
      {
        "comment_id": "4e7613a0-a9e3-4e18-8257-4d014478ac74",
        "content": "不错的建议",
        "created_at": "2020-06-08T04:47:29.298000",
        "owner": {}
      },
      {
        "comment_id": "487d5a88-efdf-4478-aa42-c0837f18ff9d",
        "content": "不错的建议",
        "created_at": "2020-06-08T04:47:29.328000",
        "owner": {}
      }
    ]
  }
}
```

## 6 用户添加反馈、需求
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/issue` | - |
| method | `POST` | - |
| header | `Authorization` | 用户 Token |
| body | `product_id（必填）` | 产品ID |
| body | `owner_id（必填）` | 创建者ID |
| body | `title（必填）` | 反馈标题 |
| body | `description（非必填）` | 反馈描述 |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "issue_id": "a7adc4b8-e569-4928-98c4-82d8037f7a6a"
  }
}
```
权限验证错误: 
```json
{
  "error_type": "permission_denied",
  "message": "没有权限",
  "ok": false
}
```

## 7 创建一个产品
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/product` | - |
| method | `POST` | - |
| header | `Authorization` | 用户 Token |
| body | `manager_id（必填）` | manager_ID |
| body | `name（必填）` | 产品名 |
| body | `description` | 产品介绍 |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "created_at": "2020-06-08T04:48:09.871147",
    "description": "产品1的介绍",
    "manager_id": "8e904f36-cd98-4588-ac09-dc23b1056876",
    "name": "产品1",
    "product_id": "d0a97333-d739-41b8-b5eb-045c3dd3fb54"
  }
}
```

## 8 查询产品
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/product/manager/{manager_id}` | - |
| method | `GET` | - |
| header | `Authorization` | 用户 Token |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "products": [
      {
        "created_at": "2020-06-08T04:48:19.746000",
        "description": "产品1的介绍",
        "manager_id": "b700c133-590a-4fa5-9e1c-2c82361f9d8a",
        "name": "产品1",
        "product_id": "7d0247ed-b2c1-45c1-80d6-76a26e962db6"
      }
    ]
  }
}
```

## 9 创建个人资料
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `v1/profile` | - |
| method | `POST` | - |
| body | `user_id(必填)` | 用户id |
| body | `nickname(必填)` | 用户昵称 |
| body | `gender` | 性别 |

正确响应: 
```json
{
  "ok": true,
  "result": {}
}
```

## 10 获取个人资料
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/profile/{user_id}` | - |
| method | `GET` | - |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "avatar": "",
    "gender": 0,
    "nickname": "tester",
    "role_id": "USER",
    "user_id": "619c1b27-161b-4aca-8426-8831ee4d1304"
  }
}
```

## 11 更新个人资料
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/profile/{user_id}` | - |
| method | `PUT` | - |
| body | `nickname` | 昵称 |
| body | `gender` | 性别 |

正确响应: 
```json
{
  "ok": true,
  "result": {}
}
```

## 12 列出标签
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/tags` | - |
| method | `GET` | - |

正确响应: 
```json
{
  "ok": true,
  "result": {
    "tags": [
      {
        "description": "Bug",
        "name": "Bug"
      },
      {
        "description": "Enhancement",
        "name": "Enhancement"
      },
      {
        "description": "Help",
        "name": "Help"
      }
    ]
  }
}
```
