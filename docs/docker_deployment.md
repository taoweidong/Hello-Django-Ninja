# Docker 部署指南

## 目录结构

```
project/
├── deploy/
│   ├── Dockerfile              # Django 应用 Docker 配置
│   ├── docker-compose.yml      # Docker Compose 编排文件
│   ├── nginx.conf             # Nginx 配置文件
│   ├── .env.prod.example      # 生产环境配置示例
│   └── docker-compose.override.yml.example # 开发环境配置示例
└── ...
```

## 部署架构

```
┌─────────────────┐    ┌────────────────┐    ┌────────────────┐
│   Internet      │───▶│    Nginx       │───▶│   Django App   │
└─────────────────┘    └────────────────┘    └────────────────┘
                              │
                              ▼
                       ┌────────────────┐
                       │   MySQL DB     │
                       └────────────────┘
```

## 服务说明

### 1. Web 服务 (Django 应用)

基于 Python 3.10 slim 镜像构建，包含：
- Django 应用
- Gunicorn WSGI 服务器
- 所有 Python 依赖

### 2. 数据库服务 (MySQL)

使用 MySQL 8.0 官方镜像，特性：
- 数据持久化存储
- 自动初始化数据库
- 安全的用户权限配置

### 3. 反向代理 (Nginx)

使用 Nginx alpine 镜像，功能：
- 静态文件服务
- 负载均衡
- SSL 终止 (可配置)

## 部署步骤

### 1. 环境准备

确保已安装 Docker 和 Docker Compose：
```bash
# 检查 Docker 版本
docker --version
docker-compose --version
```

### 2. 克隆项目

```bash
git clone https://github.com/nineaiyu/Hello-Django-Ninja.git
cd Hello-Django-Ninja
```

### 3. 配置环境变量

复制生产环境配置示例：
```bash
cp deploy/.env.prod.example .env.prod
# 根据实际需求修改 .env.prod 文件中的配置
```

### 4. 构建和启动服务

```bash
# 进入 deploy 目录并构建启动所有服务
cd deploy
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 5. 初始化数据库

首次部署需要运行数据库迁移：
```bash
# 运行数据库迁移
docker-compose exec web python manage.py migrate

# 创建超级用户
docker-compose exec web python manage.py createsuperuser
```

### 6. 访问应用

- API 文档: http://localhost/api/docs
- 管理后台: http://localhost/admin

## 管理和维护

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f web
docker-compose logs -f db
```

### 备份和恢复

```bash
# 备份数据库
docker-compose exec db mysqldump -u root -p database_name > backup.sql

# 恢复数据库
docker-compose exec db mysql -u root -p database_name < backup.sql
```

### 更新应用

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build

# 重启服务
docker-compose up -d

# 运行数据库迁移（如有需要）
docker-compose exec web python manage.py migrate
```

## 故障排除

### 常见问题

1. **端口冲突**
   ```
   ERROR: for nginx  Cannot start service nginx: driver failed programming external connectivity on endpoint
   ```
   解决方案：修改 docker-compose.yml 中的端口映射

2. **数据库连接失败**
   ```
   django.db.utils.OperationalError: (2002, "Can't connect to MySQL server")
   ```
   解决方案：检查数据库配置和网络连接

3. **权限问题**
   ```
   Permission denied: '/app/db'
   ```
   解决方案：检查数据卷权限设置

### 性能优化

1. **调整 Gunicorn 工作进程数**
   在 Dockerfile 中修改 `--workers` 参数

2. **数据库优化**
   - 调整 MySQL 配置参数
   - 添加数据库索引

3. **缓存优化**
   - 配置 Redis 缓存
   - 使用 CDN 加速静态资源

## 安全建议

1. **修改默认密码**
   - 数据库密码
   - 应用密钥
   - 管理员账户密码

2. **启用 HTTPS**
   - 配置 SSL 证书
   - 强制 HTTPS 重定向

3. **定期更新**
   - 更新基础镜像
   - 更新 Python 包
   - 应用安全补丁

4. **访问控制**
   - 限制管理后台访问
   - 配置防火墙规则
   - 使用 VPN 访问敏感接口