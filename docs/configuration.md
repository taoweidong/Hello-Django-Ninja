# 系统配置说明

## 概述

本项目使用 `pydantic-settings` 来管理配置，替代了之前使用的 `python-dotenv`。这种改进提供了更好的类型检查、验证和错误处理功能。

## 配置文件结构

项目支持多种环境的配置文件：

- `.env.dev` - 开发环境配置
- `.env.prod` - 生产环境配置
- `.env.example` - 配置文件示例

环境切换通过 `APP_ENV` 环境变量控制，默认为 `dev`。

## 配置类

配置定义在 `service/config.py` 文件中，使用 `pydantic-settings` 的 `BaseSettings` 类：

```python
class Settings(BaseSettings):
    # 基本配置
    debug: bool = Field(default=False, alias="DEBUG")
    secret_key: str = Field(default="", alias="SECRET_KEY")
    allowed_hosts: Optional[str] = Field(default="", alias="ALLOWED_HOSTS")
    
    # 数据库配置
    database_url: str = Field(default="", alias="DATABASE_URL")
    
    # JWT配置
    jwt_access_token_lifetime: int = Field(default=3600, alias="JWT_ACCESS_TOKEN_LIFETIME")
    jwt_refresh_token_lifetime: int = Field(default=86400, alias="JWT_REFRESH_TOKEN_LIFETIME")
    
    # 日志配置
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

```

## 使用方法

在代码中使用配置：

```python
from service.config import settings

# 访问配置项
print(settings.debug)
print(settings.secret_key)

# 访问列表类型的配置项
print(settings.allowed_hosts_list)
```

## 配置项说明

### 基本配置

- `DEBUG`: 调试模式开关
- `SECRET_KEY`: Django 密钥
- `ALLOWED_HOSTS`: 允许的主机列表，用逗号分隔

### 数据库配置

- `DATABASE_URL`: 数据库连接URL

### JWT配置

- `JWT_ACCESS_TOKEN_LIFETIME`: JWT访问令牌有效期（秒）
- `JWT_REFRESH_TOKEN_LIFETIME`: JWT刷新令牌有效期（秒）

### 日志配置

- `LOG_LEVEL`: 日志级别

## 环境变量优先级

配置值的优先级从高到低：

1. 环境变量
2. 环境配置文件（.env.dev 或 .env.prod）
3. 默认值

## 验证和错误处理

使用 pydantic 的验证功能，配置项会自动进行类型检查和验证。如果配置值不符合要求，会在应用启动时抛出清晰的错误信息。

## 数据库支持

本项目支持以下主流数据库：

### SQLite
SQLite是默认的开发数据库，配置简单，无需额外安装数据库服务。

配置示例：
```env
DATABASE_URL=sqlite:///db/db.sqlite3
```

### MySQL
支持MySQL 5.7及以上版本。

配置示例：
```env
DATABASE_URL=mysql://username:password@localhost:3306/database_name
```

需要安装的依赖：
```bash
pip install mysqlclient
```

### PostgreSQL
支持PostgreSQL 10及以上版本。

配置示例：
```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

需要安装的依赖：
```bash
pip install psycopg2-binary
```

## 在Django settings中使用

Django的settings.py文件会自动从配置系统中读取相关配置：

```python
from service.config import settings

# 基本配置
SECRET_KEY = settings.secret_key
DEBUG = settings.debug
ALLOWED_HOSTS = settings.allowed_hosts

# JWT配置
NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': settings.jwt_access_token_lifetime,
    'REFRESH_TOKEN_LIFETIME': settings.jwt_refresh_token_lifetime,
    # ...
}
```

## 安全建议

1. **生产环境配置**：
   - 不要在`.env.prod`文件中提交真实的密钥到版本控制系统
   - 使用强随机字符串作为SECRET_KEY
   - 限制ALLOWED_HOSTS列表

2. **敏感信息处理**：
   - 对于数据库密码等敏感信息，建议使用环境变量而不是直接写在env文件中
   - 可以在env文件中使用占位符，然后通过环境变量覆盖

3. **配置文件保护**：
   - 确保.env.prod文件不在版本控制系统中（应该在.gitignore中）
   - 限制配置文件的文件权限

## 配置文件示例

### .env.dev（开发环境）
```env
# 开发环境配置文件
DEBUG=true
SECRET_KEY=django-insecure-_)(6xwxjolsxe7d6=i$jc1f4!53zft3d!a9@w3pi(&ngepkjl&
DATABASE_URL=sqlite:///db/db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT配置
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400

# 日志配置
LOG_LEVEL=DEBUG
```

### .env.prod（生产环境）
```env
# 生产环境配置文件
DEBUG=false
SECRET_KEY=your-production-secret-key-here
# SQLite配置示例
DATABASE_URL=sqlite:///db/db.sqlite3
# MySQL配置示例
# DATABASE_URL=mysql://username:password@localhost:3306/database_name
# PostgreSQL配置示例
# DATABASE_URL=postgresql://username:password@localhost:5432/database_name
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# JWT配置
JWT_ACCESS_TOKEN_LIFETIME=1800
JWT_REFRESH_TOKEN_LIFETIME=86400

# 日志配置
LOG_LEVEL=INFO
```

## 扩展配置

如果需要添加新的配置项，可以修改`service/config.py`文件：

```python
class Settings:
    def __init__(self):
        # 添加新的配置项
        self.new_config = os.getenv("NEW_CONFIG", "default_value")
```

然后在相应的env文件中添加配置：

```env
# .env.dev 和 .env.prod
NEW_CONFIG=your_value_here