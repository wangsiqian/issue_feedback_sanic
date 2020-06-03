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
    "validate_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiMTIzNDU2QHFxLmNvbSIsInZhbGlkYXRlX2NvZGUiOiI0NTU5OTUiLCJleHAiOjE1OTExOTcwMjB9.SorObz6A_AEj9hP8BXFaQsvGGyrofJcUwuILgWMrUu4"
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
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZmRmYzAyMTEtNTEwZS00YjllLWIyOGEtMjM4Mjg0Yjk3MDViIiwicm9sZV9pZCI6IlVTRVIiLCJleHAiOjE1OTEzNjk2NjF9.iC0cGJqr21AJIyeaWAK6Bi-WfGrYrK-6g63gnlCry7I",
    "user_id": "fdfc0211-510e-4b9e-b28a-238284b9705b"
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
    "comment_id": "803fc226-eeec-4d86-b67d-9dfba5400d76"
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
        "comment_id": "2023cd84-3e6e-487e-8982-ad9a62bf6e21",
        "content": "不错的建议",
        "created_at": "2020-06-03T15:08:33.761000",
        "owner": {}
      },
      {
        "comment_id": "6a99b680-5673-4929-b97a-f29cedac6e44",
        "content": "不错的建议",
        "created_at": "2020-06-03T15:08:33.829000",
        "owner": {}
      },
      {
        "comment_id": "08e93c96-8319-4ea6-9017-d79928ecd1be",
        "content": "不错的建议",
        "created_at": "2020-06-03T15:08:33.836000",
        "owner": {}
      },
      {
        "comment_id": "0fbae338-c8f5-47f4-a46e-fe00309b88e7",
        "content": "不错的建议",
        "created_at": "2020-06-03T15:08:33.845000",
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
    "issue_id": "295b5495-ef95-4881-873a-3038990a01ea"
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
    "product_id": "2c608523-7f05-4ffa-afc7-87c30666d72e"
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
        "created_at": "2020-06-03T15:10:25.211000",
        "description": "产品1的介绍",
        "manager_id": "9edda06d-1e5d-4ff5-bc88-0d7683fa9136",
        "name": "产品1",
        "product_id": "8fbee4b8-f3ca-4a92-b6a5-d45b78e3f0a1"
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
    "user_id": "66bb44ea-c2e8-4baf-a3f8-05de2d729906"
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
