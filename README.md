# 基于 DDD (领域驱动设计) 和 django-ninja-extra 的 RBAC 系统设计方案

## 1. 项目概述

本方案旨在构建一个基于 Django 框架的 RBAC（Role-Based Access Control）权限管理系统，并严格遵循领域驱动设计 (DDD) 的原则。系统将提供用户管理、角色定义、权限分配及基于 API 的交互接口。我们将深度集成 `django-ninja` 和 `django-ninja-extra`，利用其特性来支撑 DDD 的架构思想。

**DDD 核心概念应用**:
*   **领域 (Domain)**: RBAC 系统的核心业务逻辑。
*   **子域 (Subdomain)**: 用户账户(User)、角色(Roles)、权限(Permissions) 是核心子域。
*   **限界上下文 (Bounded Context)**: 在单体应用中，整个 Django 项目可以视为一个大的限界上下文，但内部按子域划分模块以隔离关注点。未来若拆分为微服务，则每个 App 可能成为独立的限界上下文。
*   **实体 (Entity)**: 如 User, Role, Permission。
*   **值对象 (Value Object)**: 如 EmailAddress, PasswordHash (如果需要封装)。
*   **聚合 (Aggregate)**: Role 及其关联的 Permissions 可构成一个聚合；User 可能是另一个聚合根。
*   **聚合根 (Aggregate Root)**: 聚合的入口点，如 Role。
*   **仓储 (Repository)**: 负责聚合持久化的接口和实现。
*   **领域服务 (Domain Service)**: 处理跨聚合或复杂业务逻辑的服务。
*   **应用服务 (Application Service)**: 协调领域层操作，处理用例流程，供 API 层调用。

## 2. 技术选型

*   **核心框架**: Django (最新稳定版)
*   **API框架**: django-ninja + django-ninja-extra
*   **数据库**: SQLite (开发阶段), PostgreSQL/MySQL (生产推荐)
*   **认证**: Django 内置认证系统 + Token 认证 (django-ninja API)
*   **前端 (可选)**: Django Templates / React / Vue.js (本方案主要关注后端)
*   **文档**: django-ninja 自动生成的交互式 API 文档 (Swagger/OpenAPI)

## 3. 项目结构 (DDD 分层架构)
```
bash
rbac_project/
├── service/                       # 项目主目录 & 配置层
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # 项目配置
│   ├── urls.py                     # 项目根 URL 配置
│   └── wsgi.py
├── common/                         # 通用/共享层 (Cross-cutting Concerns)
│   ├── __init__.py
│   ├── exceptions.py               # 全局自定义异常
│   ├── middlewares.py              # 自定义中间件
│   └── utils.py                    # 通用工具函数
├── interfaces/                     # 接口适配层 (Interface Adapters)
│   ├── __init__.py
│   └── api/                        # API 接口实现
│       ├── __init__.py
│       ├── apps.py
│       ├── controllers/            # API 控制器 (django-ninja-extra)
│       │   ├── __init__.py
│       │   ├── auth.py             # 认证相关 API Controller
│       │   ├── users.py            # 用户管理 API Controller
│       │   ├── roles.py            # 角色管理 API Controller
│       │   └── permissions.py      # 权限管理 API Controller
│       ├── authentication.py       # API 认证类
│       ├── permissions.py          # API 权限类
│       ├── schemas.py              # API 输入输出 Schema (DTOs)
│       └── urls.py                 # API 路由配置
├── application/                    # 应用服务层 (Application Services)
│   ├── __init__.py
│   ├── services/                   # 应用服务实现
│   │   ├── __init__.py
│   │   ├── user_service.py         # 用户相关应用服务
│   │   ├── role_service.py         # 角色相关应用服务
│   │   └── permission_service.py   # 权限相关应用服务
│   └── dtos.py                     # 应用层使用的 DTO 定义 (可选，Schema也可承担)
├── domain/                         # 领域层 (Domain Layer)
│   ├── __init__.py
│   ├── models/                     # 领域模型定义 (Entities, Value Objects, Aggregates)
│   │   ├── __init__.py
│   │   ├── user.py                 # 用户领域模型 (通常复用 Django User)
│   │   ├── role.py                 # 角色领域模型
│   │   └── permission.py           # 权限领域模型 (通常复用 Django Permission)
│   ├── repositories/               # 仓储接口定义
│   │   ├── __init__.py
│   │   ├── user_repository.py      # 用户仓储接口
│   │   ├── role_repository.py      # 角色仓储接口
│   │   └── permission_repository.py # 权限仓储接口
│   ├── services/                   # 领域服务 (复杂的领域逻辑)
│   │   ├── __init__.py
│   │   └── rbac_service.py         # 核心 RBAC 逻辑 (如权限检查)
│   └── factories.py                # 领域对象工厂 (用于创建复杂对象)
├── infrastructure/                 # 基础设施层 (Infrastructure Layer)
│   ├── __init__.py
│   ├── persistence/                # 持久化实现
│   │   ├── __init__.py
│   │   ├── repos/                  # 仓储接口的具体实现 (对接 Django ORM)
│   │   │   ├── __init__.py
│   │   │   ├── user_repo_impl.py   # 用户仓储实现
│   │   │   ├── role_repo_impl.py   # 角色仓储实现
│   │   │   └── permission_repo_impl.py # 权限仓储实现
│   │   └── migrations/             # 数据库迁移文件 (由 Django 管理)
│   └── config/                     # 第三方库配置等 (如有)
├── tests/                          # 测试目录
│   ├── __init__.py
│   └── test_user_model.py          # 用户模型测试
├── manage.py                       # Django 管理命令行工具
├── requirements.txt                # 项目依赖
├── pyproject.toml                  # 项目配置文件
├── pytest.ini                      # pytest 配置
├── uv.lock                         # uv 锁文件
└── dev_tools.py                    # 开发工具脚本
```

## 4. 项目当前状态

本项目已完成以下功能实现：

### 4.1 架构实现
- [x] 完整的 DDD 分层架构搭建
- [x] 领域层模型定义 (User, Role)
- [x] 仓储接口和实现
- [x] 应用服务层实现
- [x] API 接口层实现 (基于 django-ninja-extra)

### 4.2 核心功能
- [x] 用户管理 API (创建、查询)
- [x] 角色管理 API (创建、查询)
- [x] 权限管理 API (查询)
- [x] 认证 API (登录)
- [x] 数据库迁移配置
- [x] 异常处理机制

### 4.3 开发工具
- [x] 使用 uv 进行依赖管理
- [x] pytest 测试配置
- [x] 代码格式化工具 (black)
- [x] 代码检查工具 (flake8)
- [x] 类型检查工具 (mypy)
- [x] 开发工具脚本

## 5. 快速开始

### 5.1 环境要求
- Python 3.10+
- uv (推荐) 或 pip

### 5.2 安装依赖

使用 uv (推荐):
```bash
# 安装核心依赖
uv pip install django django-ninja django-ninja-extra

# 安装开发依赖
uv pip install pytest pytest-django black flake8 mypy
```

或使用 pip:
```bash
# 安装所有依赖
pip install -r requirements.txt
```

### 5.3 数据库设置
```bash
# 运行数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 5.4 启动开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/api/docs 查看 API 文档

## 6. API 接口说明

### 6.1 认证接口
- `POST /api/auth/login/` - 用户登录

### 6.2 用户管理接口
- `POST /api/users/` - 创建用户
- `GET /api/users/{user_id}/` - 获取用户信息
- `GET /api/users/` - 获取用户列表

### 6.3 角色管理接口
- `POST /api/roles/` - 创建角色
- `GET /api/roles/{role_id}/` - 获取角色信息
- `GET /api/roles/` - 获取角色列表

### 6.4 权限管理接口
- `GET /api/permissions/{permission_id}/` - 获取权限信息
- `GET /api/permissions/` - 获取权限列表

## 7. 开发指南

### 7.1 代码质量
```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

### 7.2 运行测试
```bash
# 运行所有测试
python manage.py test

# 运行特定测试
python manage.py test tests.test_user_model
```

### 7.3 使用开发工具脚本
```bash
# 启动开发服务器
python dev_tools.py server

# 运行数据库迁移
python dev_tools.py migrate

# 运行测试
python dev_tools.py test

# 代码格式化
python dev_tools.py format

# 代码检查
python dev_tools.py check
```

## 8. 项目结构详细说明

### 8.1 领域层 (domain)
包含核心业务逻辑和领域模型：
- `models/`: 领域实体定义
- `repositories/`: 仓储接口定义
- `services/`: 领域服务实现
- `factories.py`: 领域对象工厂

### 8.2 应用服务层 (application)
负责用例编排和业务流程：
- `services/`: 应用服务实现
- `dtos.py`: 数据传输对象定义

### 8.3 基础设施层 (infrastructure)
提供技术实现细节：
- `persistence/repos/`: 仓储接口的具体实现
- `persistence/migrations/`: 数据库迁移文件

### 8.4 接口适配层 (interfaces)
负责与外部系统交互：
- `api/controllers/`: API 控制器实现
- `api/schemas.py`: API 数据结构定义
- `api/authentication.py`: 认证实现
- `api/permissions.py`: 权限控制实现

### 8.5 通用层 (common)
包含跨层共享组件：
- `exceptions.py`: 全局异常定义
- `middlewares.py`: 自定义中间件
- `utils.py`: 通用工具函数

## 9. 扩展建议

### 9.1 功能扩展
1. 添加权限分配功能
2. 实现用户角色分配
3. 添加更完善的认证机制 (JWT)
4. 实现权限继承和组权限
5. 添加审计日志功能

### 9.2 性能优化
1. 添加缓存机制
2. 实现数据库查询优化
3. 添加异步任务处理
4. 实现分页和过滤功能

### 9.3 安全增强
1. 添加输入验证
2. 实现更严格的权限控制
3. 添加速率限制
4. 实现安全头设置

## 10. 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

### 10.1 开发流程
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

### 10.2 代码规范
- 遵循 PEP 8 代码规范
- 使用类型提示
- 编写单元测试
- 保持代码简洁和可读性

## 总结

本项目提供了一个完整的基于 DDD 和 django-ninja-extra 的 RBAC 系统实现，具有清晰的架构分层和良好的可扩展性。通过使用现代化的 Python 工具链，项目具备了高效的开发体验和良好的代码质量保证。