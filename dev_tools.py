#!/usr/bin/env python
"""
开发工具脚本
提供常用的开发操作命令
"""

import os
import subprocess
import argparse
import sys


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


def setup_uv():
    """使用 uv 初始化虚拟环境并安装依赖"""
    print("使用 uv 初始化虚拟环境...")
    
    # 检查 uv 是否已安装
    if not run_command("uv --version", shell=True):
        print("未检测到 uv，请先安装 uv:")
        print("  pip install uv")
        print("或参考 README.md 中的安装说明")
        return False
    
    # 创建虚拟环境
    print("创建虚拟环境...")
    if not run_command("uv venv", shell=True):
        print("创建虚拟环境失败")
        return False
    
    # 设置 UV_LINK_MODE 环境变量以避免硬链接警告
    os.environ['UV_LINK_MODE'] = 'copy'
    
    # 安装依赖（包括开发依赖）
    print("安装项目依赖...")
    if not run_command("uv pip install -e .[dev]", shell=True):
        print("安装依赖失败，请检查:")
        print("1. 确保 pyproject.toml 和 setup.py 文件存在且配置正确")
        print("2. 查看详细错误信息并参考 docs/uv_usage.md")
        return False
    
    print("uv 虚拟环境初始化完成！")
    print("请使用以下命令激活虚拟环境:")
    if sys.platform == "win32":
        print("  Windows (cmd): .venv\\Scripts\\activate.bat")
        print("  Windows (PowerShell): .venv\\Scripts\\Activate.ps1")
    else:
        print("  macOS/Linux: source .venv/bin/activate")
    
    return True


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
            "setup-uv",
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
    elif args.command == "setup-uv":
        setup_uv()
    elif args.command == "all":
        # 运行所有设置步骤
        run_migrations()
        format_code()
        check_code()


if __name__ == "__main__":
    main()