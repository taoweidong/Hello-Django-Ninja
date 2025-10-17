"""
自定义测试运行器，用于排除有问题的测试模块
"""

from django.test.runner import DiscoverRunner


class CustomTestRunner(DiscoverRunner):
    """自定义测试运行器"""
    
    pass
