[readme.md](readme.md)

## 1 用户添加反馈、需求
**请求**: 

| 方法名 | 参数 | 描述 |
| --- | --- | --- |
| path | `/v1/issue` | - |
| method | `POST` | - |
| header | `Authentication` | 用户 Token |
| body | `product_id（必填）` | 产品ID |
| body | `owner_id（必填）` | 创建者ID |
| body | `title（必填）` | 反馈标题 |
| body | `description（非必填）` | 反馈描述 |

正确响应: 
```json
{
  "message": "",
  "ok": true,
  "result": {}
}
```
错误响应: 
```json
{
  "error_type": "issue_already_exist",
  "message": "您已经反馈过相关问题了",
  "ok": false
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