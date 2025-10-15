"""
操作日志领域模型
"""

from django.db import models
from .user import User


class OperationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    module = models.CharField(max_length=64, null=True, blank=True)
    path = models.CharField(max_length=400, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=8, null=True, blank=True)
    ipaddress = models.CharField(max_length=39, null=True, blank=True)
    browser = models.CharField(max_length=64, null=True, blank=True)
    system = models.CharField(max_length=64, null=True, blank=True)
    response_code = models.IntegerField(null=True, blank=True)
    response_result = models.TextField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_operation_logs')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_operation_logs')
    
    class Meta:
        db_table = 'system_operationlog'
    
    def __str__(self) -> str:
        return f"{self.module} - {self.path}"