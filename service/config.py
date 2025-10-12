"""
系统配置管理模块
使用pydantic-settings加载env配置文件，区分开发和生产环境
"""

import os
from pathlib import Path
from typing import List, Union, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

# 根据环境变量确定配置文件路径
APP_ENV = os.getenv("APP_ENV", "dev")
BASE_DIR = Path(__file__).resolve().parent.parent

if APP_ENV == "prod":
    ENV_FILE = BASE_DIR / ".env.prod"
else:
    ENV_FILE = BASE_DIR / ".env.dev"


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
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        if self.allowed_hosts:
            return [x.strip() for x in self.allowed_hosts.split(",")]
        return []
    
    class Config:
        env_file = ENV_FILE
        env_file_encoding = 'utf-8'
        extra = 'ignore'


# 创建配置实例
settings = Settings()