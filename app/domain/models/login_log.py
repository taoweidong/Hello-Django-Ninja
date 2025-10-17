"""
登录日志领域模型
"""

from django.db import models
from .user import User


class LoginLog(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField()
    login_status = models.BooleanField()
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    
    # 外键关系
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logs')
    
    class Meta:
        db_table = 'system_loginlog'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return f"LoginLog for user {self.user_id} at {self.login_time}"