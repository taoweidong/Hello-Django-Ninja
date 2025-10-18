"""
操作日志领域模型
"""

from django.db import models

from .base_model import generate_uuid_pk
from .user import User


class OperationLog(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    # 注意：不定义id字段，让子类模型自行定义主键字段
    created_time = models.DateTimeField(default=None, null=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    module = models.CharField(max_length=128)
    title = models.CharField(max_length=255)
    business_type = models.CharField(max_length=128)
    method = models.CharField(max_length=100)
    request_method = models.CharField(max_length=10)
    operator_type = models.CharField(max_length=50)
    oper_name = models.CharField(max_length=50)
    dept_name = models.CharField(max_length=50)
    oper_url = models.CharField(max_length=255)
    oper_ip = models.CharField(max_length=128)
    oper_location = models.CharField(max_length=255)
    oper_param = models.TextField()
    json_result = models.TextField()
    status = models.BooleanField(default=models.NOT_PROVIDED)
    error_msg = models.TextField(null=True, blank=True)
    cost_time = models.BigIntegerField()

    # 外键关系
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operation_logs')

    def __str__(self) -> str:
        return f"OperationLog {self.title} by {self.oper_name}"

    class Meta:
        db_table = 'system_operation_log'
        app_label = 'domain'
