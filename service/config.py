"""
系统配置管理模块
使用python-dotenv加载env配置文件，区分开发和生产环境
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List

# 根据环境变量确定配置文件路径
APP_ENV = os.getenv("APP_ENV", "dev")
BASE_DIR = Path(__file__).resolve().parent.parent

if APP_ENV == "prod":
    ENV_FILE = BASE_DIR / ".env.prod"
else:
    ENV_FILE = BASE_DIR / ".env.dev"

# 加载环境变量
load_dotenv(ENV_FILE)


class Settings:
    def __init__(self):
        # 基本配置
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.secret_key = os.getenv("SECRET_KEY", "")
        self.allowed_hosts = self._parse_list(os.getenv("ALLOWED_HOSTS", ""))
        
        # 数据库配置
        self.database_url = os.getenv("DATABASE_URL", "")
        
        # JWT配置
        self.jwt_access_token_lifetime = int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME", "3600"))
        self.jwt_refresh_token_lifetime = int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME", "86400"))
        
        # 日志配置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    def _parse_list(self, value: str) -> List[str]:
        if not value:
            return []
        return [x.strip() for x in value.split(",")]


# 创建配置实例
settings = Settings()