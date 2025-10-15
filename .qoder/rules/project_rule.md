---
trigger: always_on
alwaysApply: true
---

## 项目结构规范

本项目遵循领域驱动设计（DDD）模式，所有新增文件必须按照以下规范归档到对应目录：

### 项目结构 (DDD 分层架构)

```bash
project/
├── service/                       # 项目主目录 & 配置层
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # 项目配置
│   ├── urls.py                     # 项目根 URL 配置
│   └── wsgi.py
├── app/                           # 应用目录
│   ├── common/                    # 通用/共享层 (Cross-cutting Concerns)
│   │   ├── __init__.py
│   │   ├── exceptions.py          # 全局自定义异常
│   │   ├── middlewares.py         # 自定义中间件
│   │   └── utils.py               # 通用工具函数
│   ├── interfaces/                # 接口适配层 (Interface Adapters)
│   │   ├── __init__.py
│   │   └── api/                   # API 接口实现
│   │       ├── __init__.py
│   │       ├── apps.py
│   │       ├── controllers/       # API 控制器 (django-ninja-extra)
│   │       │   ├── __init__.py
│   │       │   ├── auth.py        # 认证相关 API Controller
│   │       │   ├── users.py       # 用户管理 API Controller
│   │       │   ├── roles.py       # 角色管理 API Controller
│   │       │   └── permissions.py # 权限管理 API Controller
│   │       ├── authentication.py  # API 认证类
│   │       ├── permissions.py     # API 权限类
│   │       ├── schemas.py         # API 输入输出 Schema (DTOs)
│   │       └── urls.py            # API 路由配置
│   ├── application/               # 应用服务层 (Application Services)
│   │   ├── __init__.py
│   │   ├── services/              # 应用服务实现
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py    # 用户相关应用服务
│   │   │   ├── role_service.py    # 角色相关应用服务
│   │   │   └── permission_service.py # 权限相关应用服务
│   │   └── dtos.py                # 应用层使用的 DTO 定义 (可选，Schema也可承担)
│   ├── domain/                    # 领域层 (Domain Layer)
│   │   ├── __init__.py
│   │   ├── models/                # 领域模型定义 (Entities, Value Objects, Aggregates)
│   │   │   ├── __init__.py
│   │   │   ├── user.py            # 用户领域模型 (通常复用 Django User)
│   │   │   ├── role.py            # 角色领域模型
│   │   │   └── permission.py      # 权限领域模型 (通常复用 Django Permission)
│   │   ├── repositories/          # 仓储接口定义
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py # 用户仓储接口
│   │   │   ├── role_repository.py # 角色仓储接口
│   │   │   └── permission_repository.py # 权限仓储接口
│   │   ├── services/              # 领域服务 (复杂的领域逻辑)
│   │   │   ├── __init__.py
│   │   │   └── rbac_service.py    # 核心 RBAC 逻辑 (如权限检查)
│   │   └── factories.py           # 领域对象工厂 (用于创建复杂对象)
│   └── infrastructure/            # 基础设施层 (Infrastructure Layer)
│       ├── __init__.py
│       ├── persistence/           # 持久化实现
│       │   ├── __init__.py
│       │   ├── repos/             # 仓储接口的具体实现 (对接 Django ORM)
│       │   │   ├── __init__.py
│       │   │   ├── user_repo_impl.py   # 用户仓储实现
│       │   │   ├── role_repo_impl.py   # 角色仓储实现
│       │   │   └── permission_repo_impl.py # 权限仓储实现
│       │   └── migrations/        # 数据库迁移文件 (由 Django 管理)
│       └── config/                # 第三方库配置等 (如有)
├── data/                          # 测试数据文件
├── docs/                          # 项目文档
│   └── uv_usage.md                # uv 使用指南
├── logs/                          # 日志文件
├── sql/                           # 数据库表结构
├── tests/                         # 测试目录
├── manage.py                      # Django 管理命令行工具
├── requirements.txt               # 项目依赖
├── pyproject.toml                 # 项目配置文件
├── pytest.ini                     # pytest 配置
├── uv.lock                        # uv 锁文件 (由 uv 自动生成)
└── dev_tools.py                   # 开发工具脚本
```

### 文件归档规则
1. **domain/** - 存放实体、值对象、领域服务等核心业务代码
2. **application/** - 存放应用服务、DTO、业务用例等
3. **infrastructure/** - 存放数据库访问、外部API调用等技术实现
4. **interfaces/** - 存放控制器、API接口、前端交互等

所有新增文件必须根据其职责归档到上述对应目录中，严禁随意创建目录结构。
