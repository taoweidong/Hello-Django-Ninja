# Logs Directory

This directory contains log files.

## Django 项目初始化、数据表结构创建和管理员账号创建步骤

### 1. 项目初始化

#### 1.1 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd Hello-Django-Ninja

# 创建并激活虚拟环境（推荐使用 uv）
python dev_tools.py setup-uv

# 或者手动创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
# 或使用 uv（推荐）
uv pip install -r requirements.txt
```

#### 1.2 数据库迁移
```bash
# 运行数据库迁移
python manage.py migrate

# 或使用开发工具脚本
python dev_tools.py migrate
```

这将创建以下数据表：
- `auth_group`: Django 内置组表
- `auth_group_permissions`: 组权限关联表
- `auth_permission`: 权限表
- `auth_user`: 用户表（扩展了 Django 内置 User）
- `auth_user_groups`: 用户组关联表
- `auth_user_user_permissions`: 用户权限关联表
- `domain_role`: 角色表
- `domain_role_permissions`: 角色权限关联表
- `django_admin_log`: 管理日志表
- `django_content_type`: 内容类型表
- `django_migrations`: 迁移记录表
- `django_session`: 会话表

### 2. 创建管理员账号

#### 2.1 交互式创建
```bash
# 创建超级用户
python manage.py createsuperuser

# 或使用开发工具脚本
python dev_tools.py superuser
```

按照提示输入：
- Username: `admin`
- Email address: `admin@example.com`
- Password: `admin123`
- Password (again): `admin123`

#### 2.2 非交互式创建（可选）
如果需要自动化创建管理员账号，可以使用以下脚本：

```python
# create_admin.py
import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 创建管理员用户
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("管理员账号创建成功")
else:
    print("管理员账号已存在")
```

运行脚本：
```bash
python create_admin.py
```

### 3. 启动开发服务器

```bash
# 启动开发服务器
python manage.py runserver

# 或使用开发工具脚本
python dev_tools.py server
```

访问以下地址：
- API 文档: http://127.0.0.1:8000/api/docs
- 管理后台: http://127.0.0.1:8000/admin/
- 健康检查: http://127.0.0.1:8000/api/health/

### 4. 验证安装

#### 4.1 验证数据库
```bash
# 查看所有表
python manage.py dbshell
.tables
.quit
```

#### 4.2 验证管理员账号
访问 http://127.0.0.1:8000/admin/，使用以下凭据登录：
- Username: `admin`
- Password: `admin123`

#### 4.3 验证 API
访问 http://127.0.0.1:8000/api/docs 查看 API 文档，并测试以下端点：
- `GET /api/health/` - 健康检查
- `POST /api/auth/login/` - 用户登录

### 5. 常见问题解决

#### 5.1 数据库迁移问题
如果遇到迁移问题，可以重置迁移：
```bash
# 删除迁移文件（保留 __init__.py）
rm app/domain/migrations/0*.py

# 重新创建迁移
python manage.py makemigrations
python manage.py migrate
```

#### 5.2 依赖安装问题
如果依赖安装失败：
```bash
# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements.txt
```

#### 5.3 端口占用问题
如果 8000 端口被占用：
```bash
# 使用其他端口启动
python manage.py runserver 8080
```