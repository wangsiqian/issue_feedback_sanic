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
    "validate_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiMTIzNDU2QHFxLmNvbSIsInZhbGlkYXRlX2NvZGUiOiI5MDg4ODUiLCJleHAiOjE1OTI2MzQwNzN9.T0mUKBo7VNXnqyKTSR8I5S1IAYacUOldCT0fSlu8Foo"
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
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWU1ZjJjYmUtZDUyZS00Y2I4LWEwOWEtOWVkYTQ2ZGJhMDZlIiwicm9sZV9pZCI6IlVTRVIiLCJleHAiOjE1OTI4MDY3MDF9.xVGiLLXpi5jG4Tr_zPjdkdZSrvMP2ZnHJ0si1qOxsKM",
    "user_id": "ae5f2cbe-d52e-4cb8-a09a-9eda46dba06e"
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
    "created_at": "2020-06-20T06:18:42.488378",
    "issue_id": "5e638c14-7a1b-40b6-a065-661fcba7e983",
    "receiver_id": "eb14983d-b85b-441c-998b-e0f9d87a5e42",
    "user_id": "7e1b34ec-0195-4dda-994f-0b13cc84be00"
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
        "comment_id": "25919837-ebbd-481c-a243-afcc043a40e4",
        "content": "不错的建议",
        "created_at": "2020-06-20T06:18:46.488000",
        "owner": {}
      },
      {
        "comment_id": "756ef26d-a018-4e98-a4c5-60d743f7b03a",
        "content": "不错的建议",
        "created_at": "2020-06-20T06:18:46.500000",
        "owner": {}
      },
      {
        "comment_id": "fc385e80-3bec-47fc-b893-821b1d43710a",
        "content": "不错的建议",
        "created_at": "2020-06-20T06:18:46.517000",
        "owner": {}
      },
      {
        "comment_id": "02c15948-03e1-491c-b408-3b5708e047ad",
        "content": "不错的建议",
        "created_at": "2020-06-20T06:18:46.528000",
        "owner": {}
      }
    ],
    "count": 4
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
    "issue_id": "29de0a3e-51b2-42c5-8cff-26c9acf26bf2"
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
    "created_at": "2020-06-20T06:19:59.851997",
    "description": "产品1的介绍",
    "manager_id": "a5791647-83e3-44f6-99d1-5cb954154a10",
    "name": "产品1",
    "product_id": "4985a25a-fd97-46a1-a522-6b89a2e7cd74"
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
        "created_at": "2020-06-20T06:20:06.548000",
        "description": "4",
        "manager_id": "2c8ca1d6-557c-441f-9b38-e1b57d28e539",
        "name": "4",
        "product_id": "490be88f-8742-494d-ba46-b8ac58bb1280"
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
    "user_id": "3cf30a9f-f1a7-4cba-9c74-b99bf8ce3b10"
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
        "color": "#eb4034",
        "description": "Bug",
        "name": "Bug"
      },
      {
        "color": "#eb4034",
        "description": "Enhancement",
        "name": "Enhancement"
      },
      {
        "color": "#eb4034",
        "description": "Help",
        "name": "Help"
      }
    ]
  }
}
```
