#!/usr/bin/env python
"""
开发工具脚本
提供常用的开发操作命令
"""

import os
import subprocess
import argparse
import sys
import shutil
import fnmatch


def run_command(command, shell=True):
    """运行命令并显示输出"""
    print(f"运行命令: {command}")
    try:
        # 使用通用编码处理
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # 尝试解码输出
        try:
            stdout_text = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            try:
                stdout_text = result.stdout.decode('gbk')
            except UnicodeDecodeError:
                stdout_text = result.stdout.decode('latin1')
        
        try:
            stderr_text = result.stderr.decode('utf-8')
        except UnicodeDecodeError:
            try:
                stderr_text = result.stderr.decode('gbk')
            except UnicodeDecodeError:
                stderr_text = result.stderr.decode('latin1')
        
        print(stdout_text)
        if stderr_text:
            print("输出:", stderr_text)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        # 即使命令失败，也尝试读取输出
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=False,  # 不检查返回码
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            # 尝试解码输出
            try:
                stdout_text = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    stdout_text = result.stdout.decode('gbk')
                except UnicodeDecodeError:
                    stdout_text = result.stdout.decode('latin1')
            
            try:
                stderr_text = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    stderr_text = result.stderr.decode('gbk')
                except UnicodeDecodeError:
                    stderr_text = result.stderr.decode('latin1')
            
            print(stdout_text)
            if stderr_text:
                print("输出:", stderr_text)
        except Exception as e2:
            print(f"读取输出失败: {e2}")
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


def create_default_superuser():
    """创建默认超级用户"""
    print("创建默认超级用户...")
    
    # 设置 Django 环境
    if not setup_django():
        return False
    
    try:
        # 导入 Django 模型
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # 检查是否已存在 admin 用户
        if User.objects.filter(username='admin').exists():
            print("admin 用户已存在")
            return True
        
        # 创建超级用户
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("默认超级用户创建成功!")
        print("用户名: admin")
        print("密码: admin123")
        print("请务必在生产环境中修改默认密码!")
        return True
    except Exception as e:
        print(f"创建默认超级用户失败: {e}")
        return False


def setup_database():
    """一键设置数据库：运行迁移并创建默认用户"""
    print("开始数据库设置...")
    
    # 运行数据库迁移
    if not run_migrations():
        print("数据库迁移失败")
        return False
    
    # 创建默认超级用户
    if not create_default_superuser():
        print("创建默认超级用户失败")
        return False
    
    print("\n数据库设置完成!")
    print("默认管理员账户:")
    print("  用户名: admin")
    print("  密码: admin123")
    print("\n请务必在生产环境中修改默认密码!")
    return True


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


def clean_project():
    """清理项目中的临时文件和不在版本控制中的文件"""
    print("开始清理项目...")
    
    # 读取.gitignore文件中的忽略模式
    gitignore_patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if line and not line.startswith('#'):
                    # 处理目录模式
                    if line.endswith('/'):
                        gitignore_patterns.append(line)
                    else:
                        gitignore_patterns.append(line)
    
    # 添加一些常见的临时文件模式
    additional_patterns = [
        '*.pyc',
        '__pycache__',
        '*.log',
        '*.tmp',
        '*.bak',
        '.coverage*',
        'htmlcov/',
        '.pytest_cache/',
        '*.egg-info/',
        'build/',
        'dist/',
        '.eggs/',
        '*.egg',
        '.installed.cfg',
        'uv.lock',
    ]
    
    # 合并所有模式
    all_patterns = gitignore_patterns + additional_patterns
    
    # 收集要删除的文件和目录
    items_to_delete = []
    
    for root, dirs, files in os.walk('.'):
        # 跳过.git目录
        if '.git' in root:
            continue
            
        # 检查目录
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            for pattern in all_patterns:
                if fnmatch.fnmatch(dir_name, pattern) or fnmatch.fnmatch(dir_path, pattern):
                    items_to_delete.append(dir_path)
                    break
        
        # 检查文件
        for file_name in files:
            file_path = os.path.join(root, file_name)
            for pattern in all_patterns:
                if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(file_path, pattern):
                    items_to_delete.append(file_path)
                    break
    
    # 去重并排序
    items_to_delete = sorted(list(set(items_to_delete)))
    
    if not items_to_delete:
        print("没有找到需要清理的文件或目录")
        return True
    
    print(f"找到 {len(items_to_delete)} 个需要清理的项目:")
    for item in items_to_delete:
        print(f"  - {item}")
    
    # 确认删除
    response = input("\n确认删除这些文件和目录吗? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("取消清理操作")
        return True
    
    # 执行删除
    deleted_count = 0
    for item in items_to_delete:
        try:
            if os.path.isfile(item):
                os.remove(item)
                print(f"已删除文件: {item}")
                deleted_count += 1
            elif os.path.isdir(item):
                shutil.rmtree(item)
                print(f"已删除目录: {item}")
                deleted_count += 1
        except Exception as e:
            print(f"删除 {item} 时出错: {e}")
    
    print(f"\n清理完成，共删除了 {deleted_count} 个项目")
    return True


def setup_uv():
    """使用 uv 初始化虚拟环境并安装依赖"""
    print("使用 uv 初始化虚拟环境...")
    
    # 检查 uv 是否已安装
    if not run_command("uv --version", shell=True):
        print("未检测到 uv，请先安装 uv:")
        print("  pip install uv")
        print("或参考 README.md 中的安装说明")
        return False
    
    # 检查是否存在旧的虚拟环境目录
    if os.path.exists(".venv"):
        print("检测到已存在的虚拟环境目录，正在删除...")
        try:
            shutil.rmtree(".venv")
            print("旧虚拟环境目录已删除")
        except Exception as e:
            print(f"删除旧虚拟环境目录失败: {e}")
            return False
    
    # 创建虚拟环境
    print("创建虚拟环境...")
    if not run_command("uv venv", shell=True):
        print("创建虚拟环境失败")
        return False
    
    # 设置 UV_LINK_MODE 环境变量以避免硬链接警告
    os.environ['UV_LINK_MODE'] = 'copy'
    
    # 激活虚拟环境并安装依赖
    print("激活虚拟环境并安装项目依赖...")
    if sys.platform == "win32":
        activate_cmd = ".venv\\Scripts\\activate.bat && "
    else:
        activate_cmd = "source .venv/bin/activate && "
    
    install_cmd = activate_cmd + "uv pip install -e .[dev]"
    
    if not run_command(install_cmd, shell=True):
        print("安装依赖失败，请检查:")
        print("1. 确保 pyproject.toml 和 setup.py 文件存在且配置正确")
        print("2. 查看详细错误信息并参考 docs/uv_usage.md")
        return False
    
    print("uv 虚拟环境初始化完成！")
    activate_virtualenv()
    
    return True


def activate_virtualenv():
    """根据当前操作系统，执行对应激活命令，激活虚拟环境"""
    print("激活虚拟环境...")
    
    # 检查虚拟环境是否存在
    if not os.path.exists(".venv"):
        print("错误: 未找到虚拟环境目录 .venv")
        print("请先运行 'python dev_tools.py setup-uv' 创建虚拟环境")
        return False
    
    # 根据操作系统提供相应的激活命令
    if sys.platform == "win32":
        print("Windows 系统检测到，提供两种激活方式:")
        print("\n方式1 (cmd):")
        print("  .venv\\Scripts\\activate.bat")
        print("\n方式2 (PowerShell):")
        print("  .venv\\Scripts\\Activate.ps1")
        print("\n方式3 (Git Bash):")
        print("  source .venv/Scripts/activate")
        
        # 尝试自动执行cmd激活（非交互式）
        try:
            import subprocess
            # 在Windows上，我们不能直接激活环境并保持它活跃
            # 因为子进程的环境不会影响父进程
            print("\n提示: 请手动复制上述命令到您的终端中执行")
            return True
        except Exception as e:
            print(f"自动激活尝试失败: {e}")
            return False
            
    elif sys.platform == "darwin":  # macOS
        print("macOS 系统检测到:")
        print("\n激活命令:")
        print("  source .venv/bin/activate")
        print("\n提示: 请手动复制上述命令到您的终端中执行")
        return True
        
    elif sys.platform.startswith("linux"):  # Linux
        print("Linux 系统检测到:")
        print("\n激活命令:")
        print("  source .venv/bin/activate")
        print("\n提示: 请手动复制上述命令到您的终端中执行")
        return True
        
    else:
        print(f"未知的操作系统平台: {sys.platform}")
        print("请手动激活虚拟环境:")
        if sys.platform == "win32":
            print("  Windows: .venv\\Scripts\\activate.bat")
        else:
            print("  Unix-like: source .venv/bin/activate")
        return False


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
            "activate",
            "clean",
            "setup-db",  # 新增的命令
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
    elif args.command == "activate":
        activate_virtualenv()
    elif args.command == "clean":
        clean_project()
    elif args.command == "setup-db":  # 新增的命令处理
        setup_database()
    elif args.command == "all":
        # 运行所有设置步骤
        run_migrations()
        format_code()
        check_code()


if __name__ == "__main__":
    main()