"""
API 认证类
"""

from ninja.security import HttpBearer
from django.http import HttpRequest


class TokenAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        # 简化的认证实现
        # 实际项目中需要实现基于 Token 的认证逻辑
        return None  # 简化实现