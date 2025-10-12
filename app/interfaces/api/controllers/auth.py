"""
认证相关 API Controller
"""

from ninja_extra import api_controller, http_post
from ninja import Schema
from django.contrib.auth import authenticate
from django.http import HttpRequest


class LoginSchema(Schema):
    username: str
    password: str


class TokenSchema(Schema):
    token: str


@api_controller("/auth")
class AuthController:
    @http_post("/login", response=TokenSchema)
    def login(self, request: HttpRequest, payload: LoginSchema):
        user = authenticate(username=payload.username, password=payload.password)
        if user is not None:
            # 生成并返回 token
            # 这里简化处理，实际项目中需要实现真正的 token 生成逻辑
            return {"token": "fake-token-for-demo"}
        else:
            return 401, {"message": "Invalid credentials"}
