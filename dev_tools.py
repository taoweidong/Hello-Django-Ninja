#!/usr/bin/env python
"""
开发工具脚本 - 面向对象 + loguru 日志版（已修复抽象类问题）
提供常用的开发操作命令
"""

import os
import subprocess
import argparse
import sys
import shutil
import fnmatch
from loguru import logger

class CommandRunner:
    """通用命令执行器，使用 loguru 输出"""

    @staticmethod
    def run(command, shell=True):
        logger.info(f"运行命令: {command}")
        try:
            result = subprocess.run(
                command,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout_text = CommandRunner._decode_output(result.stdout)
            stderr_text = CommandRunner._decode_output(result.stderr)

            if stdout_text.strip():
                logger.info(f"STDOUT:\n{stdout_text}")
            if stderr_text.strip():
                logger.warning(f"STDERR:\n{stderr_text}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e}")
            # 尝试获取输出
            result = subprocess.run(
                command,
                shell=shell,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout_text = CommandRunner._decode_output(result.stdout)
            stderr_text = CommandRunner._decode_output(result.stderr)
            if stdout_text.strip():
                logger.info(f"STDOUT:\n{stdout_text}")
            if stderr_text.strip():
                logger.warning(f"STDERR:\n{stderr_text}")
            return False

    @staticmethod
    def _decode_output(data: bytes) -> str:
        for encoding in ('utf-8', 'gbk', 'latin1'):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                continue
        return data.decode('utf-8', errors='replace')


class BaseCommand:
    """所有命令类的基类（普通类，非抽象）"""

    def __init__(self, runner: CommandRunner):
        self.runner = runner


class DjangoCommand(BaseCommand):
    """Django 相关命令"""

    def setup_django(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")
        try:
            import django
            django.setup()
            logger.info("Django 环境设置成功")
            return True
        except Exception as e:
            logger.error(f"Django 环境设置失败: {e}")
            return False

    def run_server(self):
        logger.info("启动开发服务器...")
        return self.runner.run("python manage.py runserver")

    def run_migrations(self):
        logger.info("运行数据库迁移...")
        self.runner.run("python manage.py makemigrations")
        return self.runner.run("python manage.py migrate")

    def create_superuser_interactive(self):
        logger.info("创建超级用户（交互式）...")
        return self.runner.run("python manage.py createsuperuser")

    def create_default_superuser(self):
        logger.info("创建默认超级用户...")
        if not self.setup_django():
            return False

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(username='admin').exists():
                logger.info("admin 用户已存在")
                return True
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            logger.success("默认超级用户创建成功!")
            logger.info("用户名: admin\n密码: admin123")
            logger.warning("请务必在生产环境中修改默认密码!")
            return True
        except Exception as e:
            logger.error(f"创建默认超级用户失败: {e}")
            return False

    def setup_database(self):
        logger.info("开始数据库设置...")
        if not self.run_migrations():
            logger.error("数据库迁移失败")
            return False
        if not self.create_default_superuser():
            logger.error("创建默认超级用户失败")
            return False
        logger.success("\n数据库设置完成!")
        logger.info("默认管理员账户:\n  用户名: admin\n  密码: admin123")
        logger.warning("\n请务必在生产环境中修改默认密码!")
        return True

    def run_tests(self):
        logger.info("运行测试...")
        return self.runner.run("python manage.py test")


class CodeQualityCommand(BaseCommand):
    """代码质量相关命令"""

    def format_code(self):
        logger.info("格式化代码...")
        return self.runner.run("black .")

    def check_code(self):
        logger.info("检查代码质量...")
        return self.runner.run("flake8 . --config=.flake8")

    def type_check(self):
        logger.info("类型检查...")
        return self.runner.run("mypy .")


class ProjectCleaner(BaseCommand):
    """项目清理命令"""

    def clean_project(self):
        logger.info("开始清理项目...")
        gitignore_patterns = self._load_gitignore()
        additional_patterns = [
            '*.pyc', '__pycache__', '*.log', '*.tmp', '*.bak',
            '.coverage*', 'htmlcov/', '.pytest_cache/', '*.egg-info/',
            'build/', 'dist/', '.eggs/', '*.egg', '.installed.cfg', 'uv.lock'
        ]
        all_patterns = gitignore_patterns + additional_patterns

        items_to_delete = self._find_items_to_delete(all_patterns)

        if not items_to_delete:
            logger.info("没有找到需要清理的文件或目录")
            return True

        logger.info(f"找到 {len(items_to_delete)} 个需要清理的项目:")
        for item in items_to_delete:
            logger.info(f"  - {item}")

        # 注意：input 前的提示仍用 print，确保用户可见
        print("\n确认删除这些文件和目录吗? (y/N): ", end='')
        response = input()
        if response.lower() not in ['y', 'yes']:
            logger.info("取消清理操作")
            return True

        deleted_count = 0
        for item in items_to_delete:
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    deleted_count += 1
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    deleted_count += 1
            except Exception as e:
                logger.error(f"删除 {item} 时出错: {e}")
        logger.success(f"\n清理完成，共删除了 {deleted_count} 个项目")
        return True

    def _load_gitignore(self):
        patterns = []
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line.rstrip('/'))
        return patterns

    def _find_items_to_delete(self, patterns):
        items = []
        for root, dirs, files in os.walk('.'):
            if '.git' in root:
                continue
            for name in dirs + files:
                path = os.path.join(root, name)
                for pat in patterns:
                    if fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(path, pat):
                        items.append(path)
                        break
        return sorted(set(items))


class UVEnvManager(BaseCommand):
    """uv 虚拟环境管理"""

    def setup_uv(self):
        logger.info("使用 uv 初始化虚拟环境...")
        if not self.runner.run("uv --version"):
            logger.error("未检测到 uv，请先安装 uv: pip install uv")
            return False

        if os.path.exists(".venv"):
            logger.info("检测到已存在的虚拟环境目录，正在删除...")
            try:
                shutil.rmtree(".venv")
            except Exception as e:
                logger.error(f"删除旧虚拟环境目录失败: {e}")
                return False

        logger.info("创建虚拟环境...")
        if not self.runner.run("uv venv"):
            return False

        os.environ['UV_LINK_MODE'] = 'copy'
        activate_cmd = ".venv\\Scripts\\activate.bat && " if sys.platform == "win32" else "source .venv/bin/activate && "
        install_cmd = activate_cmd + "uv pip install -e .[dev]"
        if not self.runner.run(install_cmd):
            logger.error("安装依赖失败，请检查 pyproject.toml 和 setup.py")
            return False

        logger.success("uv 虚拟环境初始化完成！")
        self.activate_virtualenv()
        return True

    def activate_virtualenv(self):
        logger.info("激活虚拟环境...")
        if not os.path.exists(".venv"):
            logger.error("错误: 未找到虚拟环境目录 .venv")
            return False

        if sys.platform == "win32":
            print("Windows 系统检测到，请手动执行:")
            print("  .venv\\Scripts\\activate.bat")
        else:
            print("Unix-like 系统检测到，请手动执行:")
            print("  source .venv/bin/activate")
        return True


class DevToolApp:
    """主应用类，负责命令分发"""

    def __init__(self):
        self.runner = CommandRunner()
        self.django = DjangoCommand(self.runner)
        self.code_quality = CodeQualityCommand(self.runner)
        self.cleaner = ProjectCleaner(self.runner)
        self.uv = UVEnvManager(self.runner)

    def run(self):
        parser = argparse.ArgumentParser(description="开发工具脚本")
        parser.add_argument(
            "command",
            choices=[
                "server", "migrate", "superuser", "test", "format",
                "check", "typecheck", "setup-uv", "activate", "clean",
                "setup-db", "all"
            ],
            help="要执行的命令",
        )
        args = parser.parse_args()

        cmd_map = {
            "server": self.django.run_server,
            "migrate": self.django.run_migrations,
            "superuser": self.django.create_superuser_interactive,
            "test": self.django.run_tests,
            "format": self.code_quality.format_code,
            "check": self.code_quality.check_code,
            "typecheck": self.code_quality.type_check,
            "setup-uv": self.uv.setup_uv,
            "activate": self.uv.activate_virtualenv,
            "clean": self.cleaner.clean_project,
            "setup-db": self.django.setup_database,
            "all": self._run_all,
        }

        func = cmd_map[args.command]
        func()

    def _run_all(self):
        self.django.run_migrations()
        self.code_quality.format_code()
        self.code_quality.check_code()


if __name__ == "__main__":
    app = DevToolApp()
    app.run()