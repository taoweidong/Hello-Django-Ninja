"""
认证相关 API Controller
"""

from django.contrib.auth import authenticate
from django.http import HttpRequest
from ninja import Schema
from ninja_extra import api_controller, http_post
from ninja_jwt.tokens import RefreshToken

from app.common.api_response import success, error, unauthorized
from app.api.schemas import ApiResponse


class LoginSchema(Schema):
    username: str = "admin"
    password: str = "admin123"


class TokenSchema(Schema):
    access: str
    refresh: str


@api_controller("/auth")
class AuthController:
    @http_post("/login", response=ApiResponse[TokenSchema], auth=None)  # 设置auth=None以跳过全局认证
    def login(self, request: HttpRequest, payload: LoginSchema):
        user = authenticate(username=payload.username, password=payload.password)
        if user is not None:
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            token_data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
            return success(token_data, "Login successful")
        else:
            return unauthorized("Invalid credentials")