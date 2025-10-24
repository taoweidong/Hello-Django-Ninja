"""
登录日志领域模型
"""

from django.db import models
from django.conf import settings

from .base_model import BaseModel


class LoginLog(BaseModel):
    status = models.BooleanField()
    login_type = models.IntegerField()
    ipaddress = models.CharField(max_length=45, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    system = models.CharField(max_length=255, null=True, blank=True)
    agent = models.TextField(null=True, blank=True)
    # 重写BaseModel中的creator字段，使用外键而不是字符串
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_logs",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"LoginLog for creator {self.creator} with status {self.status}"

    class Meta(BaseModel.Meta):
        db_table = 'system_login_log'
        app_label = 'domain'