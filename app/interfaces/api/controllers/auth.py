"""
认证相关 API Controller
"""

from ninja_extra import api_controller, http_post
from ninja import Schema
from django.contrib.auth import authenticate
from django.http import HttpRequest
from ninja_jwt.tokens import RefreshToken
from typing import Any


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    access: str
    refresh: str


@api_controller("/auth")
class AuthController:
    @http_post("/login", response=TokenSchema, auth=None)  # 设置auth=None以跳过全局认证
    def login(self, request: HttpRequest, payload: LoginSchema):
        user = authenticate(username=payload.username, password=payload.password)
        if user is not None:
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        else:
            # 正确地返回 401 错误响应
            return 401, {"detail": "Unauthorized"}