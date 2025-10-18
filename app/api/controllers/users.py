"""
用户管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.user_service import UserService
from app.common.exception.exceptions import BusinessException
from app.infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository
from app.api.schemas import UserOut, UserCreate, UserUpdate, ApiResponse
from app.common.api_response import success


@api_controller("/users", auth=JWTAuth())
class UsersController:
    def __init__(self):
        # 实例化仓储实现
        user_repo = DjangoORMUserRepository()
        # 实例化应用服务
        self.service = UserService(user_repo)

    @http_post("/", response=ApiResponse[UserOut])
    def create_user(self, payload: UserCreate):
        user_data = self.service.create_user(
            payload.username, payload.email, payload.password
        )
        return success(user_data, "User created successfully", 201)

    @http_get("/{user_id}", response=ApiResponse[UserOut])
    def get_user(self, user_id: int):
        # 通过service层获取用户数据
        user_data = self.service.get_user(user_id)
        if user_data:
            return success(user_data, "User retrieved successfully")
        else:
            # 这个异常将由全局异常处理器处理
            raise BusinessException("User not found")

    @http_get("/", response=ApiResponse[list[UserOut]])
    def list_users(self):
        # 通过service层获取所有用户数据
        users_data = self.service.list_users()
        return success(users_data, "Users retrieved successfully")

    @http_put("/{user_id}", response=ApiResponse[UserOut])
    def update_user(self, user_id: int, payload: UserUpdate):
        # 只传递非空值进行更新
        update_kwargs = {}
        if payload.username is not None:
            update_kwargs['username'] = payload.username
        if payload.email is not None:
            update_kwargs['email'] = payload.email
        if payload.password is not None:
            update_kwargs['password'] = payload.password
            
        user_data = self.service.update_user(
            user_id=user_id,
            **update_kwargs
        )
        return success(user_data, "User updated successfully")

    @http_delete("/{user_id}", response=ApiResponse[None])
    def delete_user(self, user_id: int):
        self.service.delete_user(user_id)
        return success(None, "User deleted successfully")