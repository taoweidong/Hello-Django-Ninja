# uv 使用指南

## uv 简介

uv 是一个极快的 Python 包和项目管理器，用 Rust 编写，速度比 pip 快 10-100 倍。

## uv.lock 文件

`uv.lock` 文件是 uv 生成的锁定文件，它确保在不同环境中安装完全相同的依赖版本，实现可重现的构建。

当您运行 `uv pip install` 命令时，uv 会自动生成或更新 uv.lock 文件。

## 常见警告及解决方案

### 1. RECORD 文件缺失警告

当出现类似以下警告时：
```
warning: Failed to uninstall package at .venv\Lib\site-packages\package-name.dist-info due to missing `RECORD` file.
```

**解决方案**：
```bash
# 清理并重新创建虚拟环境
uv cache clean
rmdir /s /q .venv
uv venv
uv pip install -e .[dev]
```

### 2. 硬链接失败警告

当出现类似以下警告时：
```
warning: Failed to hardlink files; falling back to full copy.
```

**解决方案**：
在命令行中设置环境变量：
```bash
# Windows (cmd)
set UV_LINK_MODE=copy
uv pip install -e .[dev]

# Windows (PowerShell)
$env:UV_LINK_MODE = "copy"
uv pip install -e .[dev]

# macOS/Linux
export UV_LINK_MODE=copy
uv pip install -e .[dev]
```

或者在代码中设置：
```python
import os
os.environ['UV_LINK_MODE'] = 'copy'
```

## 使用 uv 可编辑安装（推荐方式）

对于本项目，我们可以使用 `uv pip install -e .` 命令来安装所有依赖，这种方式会以可编辑模式安装项目，但不会打包项目本身：

### 1. 安装 uv

```bash
# 使用 pip 安装
pip install uv

# 或使用官方安装脚本 (推荐)
# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
# Windows (cmd)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
uv pip install -e .[dev]

# 或者仅安装基本依赖
uv pip install -e .
```

### 4. 添加新依赖

```bash
# 添加新依赖并更新 pyproject.toml
uv pip install package-name
# 然后手动将依赖添加到 pyproject.toml 中
```

## 使用 requirements.txt 安装依赖（替代方式）

如果您不想使用可编辑安装，也可以继续使用 requirements.txt 文件：

```bash
# 安装所有依赖
uv pip install -r requirements.txt
```

## 最佳实践

1. 将 `uv.lock` 文件提交到版本控制中，以确保团队成员使用相同的依赖版本
2. 使用虚拟环境隔离项目依赖
3. 定期更新依赖以获取安全补丁和新功能
4. 对于本项目，推荐使用 `uv pip install -e .[dev]` 安装所有依赖（包括开发依赖）
5. 可编辑安装允许您在开发过程中直接修改代码并立即看到更改效果
6. 遇到警告时，参考上述解决方案进行处理