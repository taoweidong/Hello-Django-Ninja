# 系统健康检查API

## 概述

本项目提供了系统健康检查API，供外部监控系统和服务状态。API提供了基本和详细的健康检查端点。

## API端点

### 基本健康检查

**端点**: `GET /api/health/`

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-12T14:30:00.123456",
  "service": "Hello-Django-Ninja",
  "version": "1.0.0"
}
```

**字段说明**:
- `status`: 服务状态，"healthy"表示健康
- `timestamp`: 响应时间戳
- `service`: 服务名称
- `version`: 服务版本

### 详细健康检查

**端点**: `GET /api/health/detailed`

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-12T14:30:00.123456",
  "service": "Hello-Django-Ninja",
  "version": "1.0.0",
  "system_info": {
    "python_version": "3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)]",
    "platform": "Windows-10-10.0.22631-SP0",
    "hostname": "MyComputer"
  },
  "database_status": "connected",
  "dependencies": {
    "django": "5.2.7",
    "django-ninja": "1.4.3"
  }
}
```

**字段说明**:
- `status`: 服务整体状态
- `timestamp`: 响应时间戳
- `service`: 服务名称
- `version`: 服务版本
- `system_info`: 系统信息
  - `python_version`: Python版本
  - `platform`: 操作系统平台
  - `hostname`: 主机名
- `database_status`: 数据库连接状态
- `dependencies`: 依赖包及其版本

## 实现详情

### Schema定义

在 `app/interfaces/api/schemas.py` 中定义了以下Schema：

1. `HealthCheckSchema`: 基本健康检查响应
2. `SystemInfoSchema`: 系统信息
3. `DetailedHealthCheckSchema`: 详细健康检查响应

### 控制器实现

在 `app/interfaces/api/controllers/health.py` 中实现了 `HealthController` 控制器：

1. `health_check()`: 基本健康检查方法
2. `detailed_health_check()`: 详细健康检查方法
3. `_check_database()`: 私有方法，检查数据库连接
4. `_get_system_info()`: 私有方法，获取系统信息
5. `_get_dependencies()`: 私有方法，获取依赖信息

### 路由配置

在 `app/interfaces/api/urls.py` 中注册了 `HealthController` 控制器。

## 使用方法

1. 启动Django开发服务器:
   ```bash
   python manage.py runserver
   ```

2. 访问健康检查端点:
   - 基本健康检查: http://127.0.0.1:8000/api/health/
   - 详细健康检查: http://127.0.0.1:8000/api/health/detailed

## 监控集成

该健康检查API可以与以下监控工具集成：

- **Prometheus**: 通过exporter定期抓取健康检查端点
- **Kubernetes**: 作为liveness和readiness探针
- **Docker**: 作为健康检查机制
- **云服务监控**: 如AWS CloudWatch、Azure Monitor等

## 扩展建议

1. 添加缓存机制以提高性能
2. 添加更详细的依赖检查
3. 添加自定义健康检查逻辑
4. 添加指标收集功能
5. 添加告警机制