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
    "validate_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoiMTIzNDU2QHFxLmNvbSIsInZhbGlkYXRlX2NvZGUiOiI0ODM4NTAiLCJleHAiOjE1OTIyMDc0MTh9.VCt5Dy092CxI3S8CahaWHPfWAJ3hRrSzYWFRahkqDkc"
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
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNjYzOGRkMjItMDViOC00Y2I4LWI0YzUtOTMzMGE4MjhlYjNiIiwicm9sZV9pZCI6IlVTRVIiLCJleHAiOjE1OTIzODAwNTl9.OH2nFS9rbYHeDB_b0YFykrbrOUaf8kp60inQhqYbqfw",
    "user_id": "6638dd22-05b8-4cb8-b4c5-9330a828eb3b"
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

## 4 修改密码
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/account/modify_password` | - |
| method | `POST` | - |
| body | `account_id（必填）` | 邮箱 |
| body | `password（必填）` | 密码 |
| body | `validate_token` | token |
| body | `validate_code` | 验证码 |

