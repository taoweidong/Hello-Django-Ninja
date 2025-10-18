# 操作日志记录中间件使用说明

## 功能概述

操作日志记录中间件用于自动记录系统中所有非查询接口的操作，并将日志信息存储到 [OperationLog](file:///E:/GitHub/Hello-Django-Ninja/Hello-Django-Ninja/app/domain/models/operation_log.py#L10-L36) 数据库表中。该中间件支持白名单配置，可以排除特定路径的日志记录。

## 功能特性

1. **自动记录操作日志**：记录所有 POST、PUT、PATCH、DELETE 请求的操作
2. **白名单支持**：可配置不需要记录日志的路径
3. **用户信息识别**：自动识别操作用户（支持 JWT 认证）
4. **详细信息记录**：记录请求参数、响应结果、操作耗时等信息
5. **模块分类**：根据请求路径自动识别操作模块

## 配置说明

中间件已自动添加到 Django 的 `MIDDLEWARE` 配置中：

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.common.middlewares.OperationLogMiddleware",  # 操作日志记录中间件
]
```

## 白名单配置

默认白名单路径包括：
- `/api/health/` - 健康检查
- `/api/health/detailed` - 详细健康检查
- `/api/auth/login` - 登录接口
- `/api/docs` - API 文档
- `/api/openapi.json` - OpenAPI 规范

如需修改白名单，可在 [middlewares.py](file:///E:/GitHub/Hello-Django-Ninja/Hello-Django-Ninja/app/common/middlewares.py) 文件中修改 `WHITE_LIST` 属性。

## 记录的HTTP方法

默认记录以下 HTTP 方法的操作：
- `POST` - 新增操作
- `PUT` - 修改操作
- `PATCH` - 部分修改操作
- `DELETE` - 删除操作

如需修改记录的方法，可在 [middlewares.py](file:///E:/GitHub/Hello-Django-Ninja/Hello-Django-Ninja/app/common/middlewares.py) 文件中修改 `RECORD_METHODS` 属性。

## 存储字段说明

操作日志记录包含以下字段：

| 字段名 | 说明 |
|-------|------|
| id | 日志ID |
| module | 操作模块 |
| title | 操作标题 |
| business_type | 业务类型（新增/修改/删除） |
| method | 请求方法和路径 |
| request_method | HTTP请求方法 |
| operator_type | 操作者类型 |
| oper_name | 操作者名称 |
| dept_name | 部门名称 |
| oper_url | 操作URL |
| oper_ip | 操作IP |
| oper_location | 操作地点 |
| oper_param | 请求参数 |
| json_result | 响应结果 |
| status | 操作状态 |
| error_msg | 错误信息 |
| cost_time | 操作耗时（毫秒） |
| user | 关联用户 |

## 自定义配置

### 修改白名单

在 [middlewares.py](file:///E:/GitHub/Hello-Django-Ninja/Hello-Django-Ninja/app/common/middlewares.py) 文件中修改 `WHITE_LIST` 列表：

```python
# 白名单路径（不记录操作日志的路径）
WHITE_LIST = [
    '/api/health/',
    '/api/health/detailed',
    '/api/auth/login',
    '/api/docs',
    '/api/openapi.json',
    # 添加自定义路径
    '/api/custom/path',
]
```

### 修改记录方法

在 [middlewares.py](file:///E:/GitHub/Hello-Django-Ninja/Hello-Django-Ninja/app/common/middlewares.py) 文件中修改 `RECORD_METHODS` 列表：

```python
# 需要记录的HTTP方法（非查询接口）
RECORD_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE', 'GET']  # 添加GET方法
```

## 测试

中间件包含完整的单元测试，可通过以下命令运行：

```bash
python -m pytest tests/test_common/test_middlewares.py -v
```

## 注意事项

1. 中间件会自动忽略白名单路径的操作记录
2. 只有认证用户（通过 JWT）的操作才会记录用户信息
3. 日志记录操作会增加请求处理时间，请在生产环境中监控性能
4. `oper_param` 和 `json_result` 字段有长度限制（2000字符），超出部分会被截断