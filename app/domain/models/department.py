"""
部门领域模型
"""

from django.db import models

from .base_model import BaseModel, generate_uuid_pk


class Department(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    rank = models.IntegerField()
    auto_bind = models.BooleanField()
    is_active = models.BooleanField()
    mode_type = models.SmallIntegerField()

    # 外键关系
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'system_department'
        app_label = 'domain'
