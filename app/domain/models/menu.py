"""
菜单领域模型
"""

from django.db import models


class Menu(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=128, unique=True)
    icon = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    component = models.CharField(max_length=255, null=True, blank=True)
    redirect = models.CharField(max_length=255, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    cache = models.BooleanField(default=False)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    remark = models.TextField(null=True, blank=True)
    
    # 外键关系
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_menus')
    modifier = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_menus')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    class Meta:
        db_table = 'system_menu'
        app_label = 'domain'
    
    def __str__(self) -> str:
        return str(self.name)