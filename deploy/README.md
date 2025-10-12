# 部署配置文件

此目录包含用于 Docker 容器化部署的配置文件。

## 文件说明

- `Dockerfile`: Django 应用的 Docker 镜像构建文件
- `docker-compose.yml`: Docker Compose 编排文件，定义了应用、数据库和反向代理服务
- `docker-compose.override.yml.example`: 开发环境的 Docker Compose 覆盖配置示例
- `nginx.conf`: Nginx 反向代理配置文件
- `.env.prod.example`: 生产环境配置文件示例

## 部署说明

请参考项目根目录下的 README.md 文件中的 Docker 部署部分，或查看 `docs/docker_deployment.md` 获取详细的部署指南。