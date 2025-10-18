"""
自定义中间件
"""

import json
import time
import uuid
from typing import Optional, Any
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import AnonymousUser
from ninja_jwt.authentication import JWTAuth
from app.domain.models.operation_log import OperationLog
from app.domain.models.user import User
from loguru import logger


class OperationLogMiddleware(MiddlewareMixin):
    """
    操作日志记录中间件
    记录所有非查询接口的操作并存储到OperationLog数据库中
    支持白名单配置
    """

    # 白名单路径（不记录操作日志的路径）
    WHITE_LIST = {
        '/api/health/',
        '/api/health/detailed',
        '/api/auth/login',
        '/api/docs',
        '/api/openapi.json',
    }

    # 需要记录的HTTP方法（非查询接口）
    RECORD_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request: HttpRequest):
        start_time = time.time()
        response = self.get_response(request)
        self._record_operation_log(request, response, start_time)
        return response

    def _should_record_log(self, request: HttpRequest) -> bool:
        """判断是否应该记录操作日志"""
        return (
            request.path_info not in self.WHITE_LIST
            and request.method in self.RECORD_METHODS
        )

    def _get_current_user(self, request: HttpRequest) -> Optional[User]:
        """获取当前用户"""
        user_attr = getattr(request, 'user', None)
        if isinstance(user_attr, User):
            return user_attr

        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ', 1)[1]
                jwt_auth = JWTAuth()
                user = jwt_auth.authenticate(request, token)
                if isinstance(user, User):
                    return user
        except Exception as e:
            logger.warning(f"Failed to get user from JWT token: {e}")

        return None

    def _get_client_ip(self, request: HttpRequest) -> str:
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '') or ''

    def _get_user_agent(self, request: HttpRequest) -> str:
        """获取用户代理信息"""
        return request.META.get('HTTP_USER_AGENT', '')

    def _safe_decode_body(self, body: bytes) -> str:
        """安全地解码请求或响应体"""
        try:
            return body.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            return ''

    def _get_request_params(self, request: HttpRequest) -> str:
        """获取请求参数（限制长度）"""
        try:
            if request.method == 'GET':
                return json.dumps(dict(request.GET), ensure_ascii=False)
            elif request.method in self.RECORD_METHODS:
                if hasattr(request, 'body'):
                    return self._safe_decode_body(request.body)
        except Exception as e:
            logger.warning(f"Failed to get request params: {e}")
        return ''

    def _get_response_content(self, response: HttpResponse) -> str:
        """获取响应内容（限制长度）"""
        try:
            if hasattr(response, 'content'):
                return self._safe_decode_body(response.content)
        except Exception as e:
            logger.warning(f"Failed to get response content: {e}")
        return ''

    def _get_module_name(self, path: str) -> str:
        """根据路径获取模块名称"""
        path_module_map = {
            '/api/users': '用户管理',
            '/api/roles': '角色管理',
            '/api/permissions': '权限管理',
            '/api/departments': '部门管理',
            '/api/menus': '菜单管理',
            '/api/system-configs': '系统配置',
            '/api/login-logs': '登录日志',
            '/api/operation-logs': '操作日志',
        }
        for prefix, module in path_module_map.items():
            if path.startswith(prefix):
                return module
        return '系统管理'

    def _get_business_type(self, method: str) -> str:
        """根据HTTP方法获取业务类型"""
        return {
            'POST': '新增',
            'PUT': '修改',
            'PATCH': '修改',
            'DELETE': '删除'
        }.get(method, '其他')

    def _record_operation_log(self, request: HttpRequest, response: HttpResponse, start_time: float):
        """记录操作日志到数据库"""
        if not self._should_record_log(request):
            return

        try:
            cost_time = int((time.time() - start_time) * 1000)
            user = self._get_current_user(request)
            client_ip = self._get_client_ip(request)
            user_agent = self._get_user_agent(request)
            request_params = self._get_request_params(request)
            response_content = self._get_response_content(response)

            module = self._get_module_name(request.path_info)
            method = request.method or ''
            business_type = self._get_business_type(method)

            operation_log = OperationLog(
                id=str(uuid.uuid4()).replace('-', ''),
                module=module,
                title=f"{method} {request.path_info}",
                business_type=business_type,
                method=f"{method} {request.path_info}",
                request_method=method,
                operator_type='后台用户',
                oper_name=getattr(user, 'username', 'Anonymous'),
                dept_name='',
                oper_url=request.path_info or '',
                oper_ip=client_ip,
                oper_location='',
                oper_param=request_params[:2000],
                json_result=response_content[:2000],
                status=(getattr(response, 'status_code', 0) < 400),
                error_msg='' if getattr(response, 'status_code', 0) < 400 else f"Status code: {response.status_code}",
                cost_time=cost_time,
                user=user
            )
            operation_log.save()
            logger.info(f"Operation log recorded: {method} {request.path_info}")

        except Exception as e:
            logger.error(f"Failed to record operation log: {e}")