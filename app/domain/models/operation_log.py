"""
操作日志领域模型
"""

from django.db import models
from .user import User


class OperationLog(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
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
    status = models.BooleanField(default=True)
    error_msg = models.TextField(null=True, blank=True)
    cost_time = models.BigIntegerField()
    
    # 外键关系
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operation_logs')
    
    class Meta:
        db_table = 'system_operation_log'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return f"OperationLog {self.title} by {self.oper_name}"