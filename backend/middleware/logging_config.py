"""
日志配置
提供统一的日志配置和管理
"""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


# 创建logs目录
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class LogConfig:
    """日志配置类"""
    
    # 日志级别
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # 日志文件配置
    APP_LOG_FILE = LOGS_DIR / "app.log"
    ERROR_LOG_FILE = LOGS_DIR / "error.log"
    ACCESS_LOG_FILE = LOGS_DIR / "access.log"
    
    # 文件大小限制（10MB）
    MAX_BYTES = 10 * 1024 * 1024
    
    # 备份文件数量
    BACKUP_COUNT = 5


def setup_logging():
    """设置日志配置"""
    
    # 创建根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LogConfig.LOG_LEVEL))
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(
        LogConfig.LOG_FORMAT,
        datefmt=LogConfig.DATE_FORMAT
    )
    
    # 1. 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 2. 应用日志文件处理器（所有日志）
    app_handler = RotatingFileHandler(
        LogConfig.APP_LOG_FILE,
        maxBytes=LogConfig.MAX_BYTES,
        backupCount=LogConfig.BACKUP_COUNT,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(formatter)
    root_logger.addHandler(app_handler)
    
    # 3. 错误日志文件处理器（仅ERROR及以上）
    error_handler = RotatingFileHandler(
        LogConfig.ERROR_LOG_FILE,
        maxBytes=LogConfig.MAX_BYTES,
        backupCount=LogConfig.BACKUP_COUNT,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # 4. 访问日志处理器（按天轮转）
    access_handler = TimedRotatingFileHandler(
        LogConfig.ACCESS_LOG_FILE,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(formatter)
    
    # 创建访问日志器
    access_logger = logging.getLogger('access')
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    
    logging.info("日志系统初始化完成")


def get_logger(name: str) -> logging.Logger:
    """
    获取日志器
    
    Args:
        name: 日志器名称（通常使用__name__）
    
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)


# 日志装饰器

def log_function_call(func):
    """记录函数调用的装饰器"""
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"调用函数: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {e}")
            raise
    
    return wrapper


def log_execution_time(func):
    """记录函数执行时间的装饰器"""
    import functools
    import time
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{func.__name__} 执行时间: {duration:.3f}秒")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} 执行失败 (耗时: {duration:.3f}秒): {e}")
            raise
    
    return wrapper


# 初始化日志系统
setup_logging()
