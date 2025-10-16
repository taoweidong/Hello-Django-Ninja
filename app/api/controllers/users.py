"""
用户管理 API Controller
"""

from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from ninja_jwt.authentication import JWTAuth

from app.application.services.user_service import UserService
from app.common.exceptions import BusinessException
from app.infrastructure.persistence.repos.user_repo_impl import DjangoORMUserRepository
from app.api.schemas import UserOut, UserCreate, UserUpdate, ApiResponse
from app.common.api_response import success, error, not_found


@api_controller("/users", auth=JWTAuth())
class UsersController:
    def __init__(self):
        # 实例化仓储实现
        user_repo = DjangoORMUserRepository()
        # 实例化应用服务
        self.service = UserService(user_repo)

    @http_post("/", response=ApiResponse[UserOut])
    def create_user(self, payload: UserCreate):
        try:
            user_data = self.service.create_user(
                payload.username, payload.email, payload.password
            )
            return success(user_data, "User created successfully", 201)
        except BusinessException as e:
            return error(str(e), 400)

    @http_get("/{user_id}", response=ApiResponse[UserOut])
    def get_user(self, user_id: int):
        # 通过service层获取用户数据
        try:
            user_data = self.service.get_user(user_id)
            if user_data:
                return success(user_data, "User retrieved successfully")
            else:
                return not_found("User not found")
        except BusinessException as e:
            return error(str(e), 400)

    @http_get("/", response=ApiResponse[list[UserOut]])
    def list_users(self):
        # 通过service层获取所有用户数据
        try:
            users_data = self.service.list_users()
            return success(users_data, "Users retrieved successfully")
        except Exception as e:
            return error(str(e), 400)

    @http_put("/{user_id}", response=ApiResponse[UserOut])
    def update_user(self, user_id: int, payload: UserUpdate):
        try:
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
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)

    @http_delete("/{user_id}", response=ApiResponse[None])
    def delete_user(self, user_id: int):
        try:
            self.service.delete_user(user_id)
            return success(None, "User deleted successfully")
        except BusinessException as e:
            return error(str(e), 400)
        except Exception as e:
            return error(str(e), 400)