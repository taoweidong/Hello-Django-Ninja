"""
登录日志领域模型
"""

from django.db import models
from .base_model import BaseModel
from .user import User


class LoginLog(BaseModel):
    id = models.CharField(max_length=32, primary_key=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    login_status = models.BooleanField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    
    # 外键关系
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    
    def __str__(self) -> str:
        return f"LoginLog for user {self.user} at {self.login_time}"
    
    class Meta:
        db_table = 'system_loginlog'
        app_label = 'domain'