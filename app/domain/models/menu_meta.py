"""
菜单元数据领域模型
"""

from django.db import models

from .base_model import BaseModel


class MenuMeta(BaseModel):
    title = models.CharField(max_length=128)
    icon = models.CharField(max_length=100, null=True, blank=True)
    r_svg_name = models.CharField(max_length=100, null=True, blank=True)
    is_show_menu = models.BooleanField(default=True)
    is_show_parent = models.BooleanField(default=True)
    is_keepalive = models.BooleanField(default=True)
    frame_url = models.CharField(max_length=255, null=True, blank=True)
    frame_loading = models.BooleanField(default=False)
    transition_enter = models.CharField(max_length=100, null=True, blank=True)
    transition_leave = models.CharField(max_length=100, null=True, blank=True)
    is_hidden_tag = models.BooleanField(default=False)
    fixed_tag = models.BooleanField(default=False)
    dynamic_level = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    cache = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    remark = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.title)
    
    class Meta:
        db_table = 'system_menu_meta'
        app_label = 'domain'