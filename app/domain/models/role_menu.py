"""
角色菜单关联模型
"""

from django.db import models
from .role import Role
from .menu import Menu


class RoleMenu(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'system_userrole_menu'
        unique_together = ('role', 'menu')
    
    def __str__(self) -> str:
        return f"{self.role} - {self.menu}"