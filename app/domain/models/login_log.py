"""
用户登录日志领域模型
"""

from django.db import models
from .user import User


class LoginLog(models.Model):
    LOGIN_TYPES = (
        (1, '普通登录'),
        (2, '微信登录'),
        (3, 'QQ登录'),
    )
    
    id = models.BigAutoField(primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    status = models.BooleanField()
    ipaddress = models.CharField(max_length=39, null=True, blank=True)
    browser = models.CharField(max_length=64, null=True, blank=True)
    system = models.CharField(max_length=64, null=True, blank=True)
    agent = models.CharField(max_length=128, null=True, blank=True)
    login_type = models.SmallIntegerField()
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_login_logs')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_login_logs')
    
    class Meta:
        db_table = 'system_userloginlog'
    
    def __str__(self) -> str:
        return f"{self.creator} - {self.created_time}"