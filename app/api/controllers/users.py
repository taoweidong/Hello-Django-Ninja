"""
用户管理 API Controller
"""

from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.user_service import UserService
from app.common.exceptions import BusinessException
from app.domain.models.user import User
from app.infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository
from app.api.schemas import UserOut, UserCreate, UserUpdate


@api_controller("/users", auth=JWTAuth())
class UsersController:
    def __init__(self):
        # 实例化仓储实现
        user_repo = DjangoORMUserRepository()
        # 实例化应用服务
        self.service = UserService(user_repo)

    @http_post("/", response={201: UserOut})
    def create_user(self, payload: UserCreate):
        try:
            user_data = self.service.create_user(
                payload.username, payload.email, payload.password
            )
            return 201, user_data
        except BusinessException as e:
            return 400, {"message": str(e)}

    @http_get("/{user_id}", response=UserOut)
    def get_user(self, user_id: int):
        # 实现获取用户的逻辑
        try:
            # 注意：这里应该通过service层获取用户数据
            user = User.objects.get(id=user_id)
            return UserOut(
                id=user.id,
                username=user.username,
                email=user.email
            )
        except ObjectDoesNotExist:
            return 404, {"message": "User not found"}

    @http_get("/", response=list[UserOut])
    def list_users(self):
        # 实现列出所有用户的逻辑
        users = User.objects.all()
        return [
            UserOut(
                id=user.id,
                username=user.username,
                email=user.email
            )
            for user in users
        ]

    @http_put("/{user_id}", response=UserOut)
    def update_user(self, user_id: int, payload: UserUpdate):
        try:
            UserModel = apps.get_model("domain", "User")
            user = UserModel.objects.get(id=user_id)
            if payload.username is not None:
                user.username = payload.username
            if payload.email is not None:
                user.email = payload.email
            if payload.password is not None:
                user.set_password(payload.password)
            user.save()
            return UserOut(
                id=user.id,
                username=user.username,
                email=user.email
            )
        except ObjectDoesNotExist:
            return 404, {"message": "User not found"}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{user_id}", response={204: None})
    def delete_user(self, user_id: int):
        try:
            UserModel = apps.get_model("domain", "User")
            user = UserModel.objects.get(id=user_id)
            user.delete()
            return 204, None
        except ObjectDoesNotExist:
            return 404, {"message": "User not found"}
        except Exception as e:
            return 400, {"message": str(e)}