"""
登录日志领域模型
"""

from django.db import models

from .base_model import BaseModel


class LoginLog(BaseModel):
    status = models.BooleanField()
    login_type = models.IntegerField()
    ipaddress = models.CharField(max_length=45, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    system = models.CharField(max_length=255, null=True, blank=True)
    agent = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"LoginLog for creator {self.creator} with status {self.status}"

    class Meta(BaseModel.Meta):
        db_table = 'system_login_log'
        app_label = 'domain'
