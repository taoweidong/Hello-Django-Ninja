"""
抽象基类模型，包含所有模型的公共字段
"""
import uuid
import threading
from typing import Optional

from django.db import models
from django.utils import timezone


def generate_uuid_pk():
    """生成UUID主键"""
    return str(uuid.uuid4()).replace('-', '')


# 线程本地存储，用于保存当前用户信息
_thread_locals = threading.local()


def set_current_user(username: str):
    """设置当前用户"""
    _thread_locals.user = username


def get_current_user() -> Optional[str]:
    """获取当前用户"""
    return getattr(_thread_locals, 'user', None)


class BaseModel(models.Model):
    """
    抽象基类模型，包含所有模型的公共字段
    """
    id = models.CharField(max_length=32, primary_key=True, default=generate_uuid_pk)
    # 注意：不定义id字段，让子类模型自行定义主键字段
    created_time = models.DateTimeField(default=None, null=True)
    updated_time = models.DateTimeField(default=None, null=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    creator = models.CharField(max_length=128, null=True, blank=True)  # 存储用户名而非外键
    modifier = models.CharField(max_length=128, null=True, blank=True)  # 存储用户名而非外键

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # 更新updated_time为当前时间
        self.updated_time = timezone.now()

        # 如果是新记录且created_time未设置，则设置为当前时间
        if not self.created_time:
            self.created_time = timezone.now()

        # 调用父类的save方法
        super().save(*args, **kwargs)