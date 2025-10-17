"""
部门领域模型
"""

from django.db import models


class Department(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    rank = models.IntegerField()
    auto_bind = models.BooleanField()
    is_active = models.BooleanField()
    mode_type = models.SmallIntegerField()
    
    # 外键关系
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_departments')
    modifier = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_departments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    class Meta:
        db_table = 'system_deptinfo'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return str(self.name)