"""
用户管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, permissions
from ninja import Schema
from application.services.user_service import UserService
from interfaces.api.schemas import UserOut, UserCreate
from common.exceptions import BusinessException
from infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository


@api_controller("/users", permissions=[permissions.IsAuthenticated])
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

    @http_get("/{int:user_id}", response=UserOut)
    def get_user(self, user_id: int):
        # 实现获取用户的逻辑
        pass

    @http_get("/", response=list[UserOut])
    def list_users(self):
        # 实现列出所有用户的逻辑
        pass
