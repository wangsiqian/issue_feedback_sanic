# 软件反馈收集系统

### 开发需遵循以下几点要求

- 按领域对项目进行拆分，确定好领域边界
- 编写实现功能的单元测试和集成测试
- 建议先设计 api，然后写测试，遵循 TDD 开发

### 添加 api

- 在 example.models 中添加需要的 model
- 在 example.api 中添加暴露给客户端的 api 接口
- 在 example.service 中添加服务接口，api 是 service 的子集
- 在 example.exceptions 中添加自定义异常
- 在 example.router 中添加路由
- 在 tests 中添加测试，按领域划分

### 如何运行
```shell script
bash start_develop.sh
```
