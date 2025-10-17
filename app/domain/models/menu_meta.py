"""
菜单元数据领域模型
"""

from django.db import models


class MenuMeta(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    title = models.CharField(max_length=128)
    icon = models.CharField(max_length=100, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    cache = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    remark = models.TextField(null=True, blank=True)
    
    # 外键关系
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_menu_metas')
    modifier = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_menu_metas')
    
    class Meta:
        db_table = 'system_menu_meta'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return str(self.title)