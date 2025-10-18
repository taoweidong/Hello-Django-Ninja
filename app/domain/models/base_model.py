"""
抽象基类模型，包含所有模型的公共字段
"""
import uuid

from django.db import models
from django.utils import timezone


def generate_uuid_pk():
    """生成UUID主键"""
    return str(uuid.uuid4()).replace('-', '')


class BaseModel(models.Model):
    """
    抽象基类模型，包含所有模型的公共字段
    """
    # 注意：不定义id字段，让子类模型自行定义主键字段
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=256, null=True, blank=True)
    creator = models.CharField(max_length=128, null=True, blank=True)  # 存储用户名而非外键
    modifier = models.CharField(max_length=128, null=True, blank=True)  # 存储用户名而非外键

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # 在保存时更新updated_time
        self.updated_time = timezone.now()
        super().save(*args, **kwargs)
