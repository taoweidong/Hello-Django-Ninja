"""
角色菜单关联领域模型
"""

from django.db import models

from .base_model import BaseModel, generate_uuid_pk


class RoleMenu(BaseModel):
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    
    # 外键关系
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role_menus')
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name='role_menus')
    
    def __str__(self) -> str:
        return f"RoleMenu for role {self.role} and menu {self.menu}"
    
    class Meta:
        db_table = 'system_role_menu'
        app_label = 'domain'