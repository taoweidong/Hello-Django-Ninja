"""
用户管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.user_service import UserService
from app.common.exceptions import BusinessException
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
        # 通过service层获取用户数据
        try:
            user_data = self.service.get_user(user_id)
            return user_data
        except BusinessException as e:
            return 400, {"message": str(e)}

    @http_get("/", response=list[UserOut])
    def list_users(self):
        # 通过service层获取所有用户数据
        try:
            users_data = self.service.list_users()
            return users_data
        except Exception as e:
            return 400, {"message": str(e)}

    @http_put("/{user_id}", response=UserOut)
    def update_user(self, user_id: int, payload: UserUpdate):
        try:
            user_data = self.service.update_user(
                user_id=user_id,
                username=payload.username,
                email=payload.email,
                password=payload.password
            )
            return user_data
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}

    @http_delete("/{user_id}", response={204: None})
    def delete_user(self, user_id: int):
        try:
            self.service.delete_user(user_id)
            return 204, None
        except BusinessException as e:
            return 400, {"message": str(e)}
        except Exception as e:
            return 400, {"message": str(e)}