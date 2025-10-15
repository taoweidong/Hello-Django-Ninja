"""
菜单元数据领域模型
"""

from django.db import models
from .user import User


class MenuMeta(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    r_svg_name = models.CharField(max_length=255, null=True, blank=True)
    is_show_menu = models.BooleanField()
    is_show_parent = models.BooleanField()
    is_keepalive = models.BooleanField()
    frame_url = models.CharField(max_length=255, null=True, blank=True)
    frame_loading = models.BooleanField()
    transition_enter = models.CharField(max_length=255, null=True, blank=True)
    transition_leave = models.CharField(max_length=255, null=True, blank=True)
    is_hidden_tag = models.BooleanField()
    fixed_tag = models.BooleanField()
    dynamic_level = models.IntegerField()
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_menu_metas')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_menu_metas')
    
    class Meta:
        db_table = 'system_menumeta'
    
    def __str__(self) -> str:
        return str(self.title or self.id)