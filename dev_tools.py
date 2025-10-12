#!/usr/bin/env python
"""
开发工具脚本
提供常用的开发操作命令
"""

import os
import subprocess
import argparse


def run_command(command, shell=True):
    """运行命令并显示输出"""
    print(f"运行命令: {command}")
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        print("错误输出:", e.stderr)
        return False


def setup_django():
    """设置 Django 环境"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
    try:
        import django

        django.setup()
        print("Django 环境设置成功")
        return True
    except Exception as e:
        print(f"Django 环境设置失败: {e}")
        return False


def run_server():
    """启动开发服务器"""
    print("启动开发服务器...")
    return run_command("python manage.py runserver")


def run_migrations():
    """运行数据库迁移"""
    print("运行数据库迁移...")
    return run_command("python manage.py migrate")


def create_superuser():
    """创建超级用户"""
    print("创建超级用户...")
    return run_command("python manage.py createsuperuser")


def run_tests():
    """运行测试"""
    print("运行测试...")
    # 使用 Django 测试命令
    return run_command("python manage.py test")


def format_code():
    """格式化代码"""
    print("格式化代码...")
    return run_command("black .")


def check_code():
    """检查代码质量"""
    print("检查代码质量...")
    return run_command("flake8 . --config=.flake8")


def type_check():
    """类型检查"""
    print("类型检查...")
    return run_command("mypy .")


def main():
    parser = argparse.ArgumentParser(description="开发工具脚本")
    parser.add_argument(
        "command",
        choices=[
            "server",
            "migrate",
            "superuser",
            "test",
            "format",
            "check",
            "typecheck",
            "all",
        ],
        help="要执行的命令",
    )

    args = parser.parse_args()

    if args.command == "server":
        run_server()
    elif args.command == "migrate":
        run_migrations()
    elif args.command == "superuser":
        create_superuser()
    elif args.command == "test":
        run_tests()
    elif args.command == "format":
        format_code()
    elif args.command == "check":
        check_code()
    elif args.command == "typecheck":
        type_check()
    elif args.command == "all":
        # 运行所有设置步骤
        run_migrations()
        format_code()
        check_code()


if __name__ == "__main__":
    main()
