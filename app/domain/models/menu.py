"""
菜单领域模型
"""

from django.db import models

from .base_model import BaseModel


class Menu(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    menu_type = models.SmallIntegerField()
    rank = models.IntegerField()
    path = models.CharField(max_length=255, null=True, blank=True)
    component = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField()
    method = models.CharField(max_length=10, null=True, blank=True)
    meta_id = models.CharField(max_length=32)
    parent_id = models.CharField(max_length=32, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    redirect = models.CharField(max_length=255, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    cache = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    remark = models.TextField(null=True, blank=True)

    # 外键关系 (移除parent字段，因为我们已经定义了parent_id)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return str(self.name)

    class Meta(BaseModel.Meta):
        db_table = 'system_menu'
        app_label = 'domain'