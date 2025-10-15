"""
菜单领域模型
"""

from django.db import models
from .user import User
from .menu_meta import MenuMeta


class Menu(models.Model):
    MENU_TYPES = (
        (1, '目录'),
        (2, '菜单'),
        (3, '按钮'),
    )
    
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    description = models.CharField(max_length=256, null=True, blank=True)
    menu_type = models.SmallIntegerField()
    name = models.CharField(max_length=128, unique=True)
    rank = models.IntegerField()
    path = models.CharField(max_length=255)
    component = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField()
    method = models.CharField(max_length=10, null=True, blank=True)
    
    # 外键关系
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_menus')
    modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_menus')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    meta = models.ForeignKey(MenuMeta, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'system_menu'
    
    def __str__(self) -> str:
        return str(self.name)