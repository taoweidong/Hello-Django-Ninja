# 日志配置说明

## 概述

本项目使用 [loguru](https://github.com/Delgan/loguru) 库进行日志记录，提供了比标准 Python logging 模块更简洁、更强大的日志功能。日志配置会自动拦截并替换标准logging模块的功能，使整个项目统一使用loguru进行日志记录。

## 日志配置

日志配置文件位于 `service/logging_config.py`，配置了以下功能：

1. **日志级别分离**：不同级别的日志分别记录到不同的文件中
2. **日志轮转**：当日志文件达到100MB时自动轮转
3. **日志保留**：根据日志级别设置不同的保留时间
4. **日志格式**：统一的日志格式，包含时间、级别、模块、函数、行号和消息
5. **标准logging模块拦截**：自动拦截标准logging模块的日志记录，统一使用loguru处理

### 日志文件说明

- `logs/debug.log`：记录 DEBUG 及以上级别的日志，保留10天
- `logs/info.log`：记录 INFO 及以上级别的日志，保留30天
- `logs/warning.log`：记录 WARNING 及以上级别的日志，保留60天
- `logs/error.log`：记录 ERROR 及以上级别的日志，保留90天

## 使用方法

在任何需要记录日志的Python文件中，只需导入配置好的logger：

```python
from service.logging_config import logger

# 记录不同级别的日志
logger.debug("这是一条调试信息")
logger.info("这是一条普通信息")
logger.warning("这是一条警告信息")
logger.error("这是一条错误信息")
```

也可以继续使用标准的logging模块，它们会被自动拦截并使用loguru处理：

```python
import logging

logger = logging.getLogger(__name__)
logger.info("这条信息也会被loguru记录")
logger.error("这条错误信息同样会被loguru记录")
```

## 日志格式

日志格式如下：

```
2025-10-12 16:24:07.710 | INFO     | __main__:<module>:22 - This is an info message
```

包含以下信息：
- 时间戳：YYYY-MM-DD HH:mm:ss.SSS
- 日志级别：DEBUG/INFO/WARNING/ERROR
- 模块名：记录日志的模块
- 函数名：记录日志的函数
- 行号：记录日志的代码行号
- 消息：日志内容

## 配置详情

### 日志轮转
- 当日志文件大小达到100MB时自动创建新的日志文件
- 避免单个日志文件过大导致的问题

### 日志保留
- DEBUG日志保留10天
- INFO日志保留30天
- WARNING日志保留60天
- ERROR日志保留90天

### 异步写入
- 使用 `enqueue=True` 参数启用异步写入，避免日志记录阻塞主程序执行

### 异常追踪
- ERROR级别的日志包含完整的异常追踪信息
- DEBUG级别的日志包含详细的诊断信息

### 标准logging模块拦截
- 通过 `InterceptHandler` 类拦截标准logging模块的所有日志记录
- 无论使用loguru还是标准logging，都会统一使用loguru的配置进行处理
- 保证整个项目日志格式和存储的一致性