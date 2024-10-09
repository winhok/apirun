# -*- coding:utf-8 -*-
import logging
import os
import time
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
from typing import Dict, Any

import colorlog

# 获取日志文件存储路径
# 使用os.path.join确保跨平台兼容性
logs_path = os.path.join(os.path.dirname(__file__), '..', 'logs')
# 创建日志目录,如果目录已存在则不会报错
os.makedirs(logs_path, exist_ok=True)

# 日志文件名按日期命名
# 格式为: test.YYYYMMDD.log
logfile_name = os.path.join(
    logs_path, 'test.{}.log'.format(time.strftime('%Y%m%d')))


class HandleLogs:
    """处理日志配置和输出的类"""

    @staticmethod
    def setting_log_color() -> colorlog.ColoredFormatter:
        """
        设置彩色日志输出格式
        :return: 彩色日志输出格式对象
        """
        # 定义不同日志级别的颜色
        log_color_config: Dict[str, str] = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'CRITICAL': 'red'
        }
        # 创建彩色日志格式器
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s %(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - '
            '%(message)s',
            log_colors=log_color_config)

        return formatter

    @classmethod
    def output_logs(cls):
        """
        配置日志输出到控制台和文件
        :return: 日志记录器对象
        """
        # 创建日志记录器
        logger: logging.Logger = logging.getLogger(__name__)
        # 获取彩色日志输出格式
        steam_format: colorlog.ColoredFormatter = HandleLogs.setting_log_color()

        # 防止重复打印日志
        if not logger.handlers:
            # 设置日志记录器的日志级别为DEBUG
            logger.setLevel(logging.DEBUG)
            # 创建文件日志格式器
            log_format: logging.Formatter = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s')

            # 配置控制台日志处理器
            sh: logging.StreamHandler = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)  # 设置控制台日志处理器的日志级别为DEBUG
            sh.setFormatter(steam_format)  # 设置控制台日志处理器的格式
            logger.addHandler(sh)  # 将控制台日志处理器添加到日志记录器中

            # 配置文件日志处理器
            try:
                # 创建RotatingFileHandler对象
                # maxBytes=5242880: 文件大小上限为5MB
                # backupCount=7: 最多保留7个备份文件
                fh: logging.RotatingFileHandler = RotatingFileHandler(
                    filename=logfile_name, mode='a', maxBytes=5242880, backupCount=7, encoding='utf-8')
                fh.setLevel(logging.DEBUG)  # 设置文件日志处理器的日志级别为DEBUG
                fh.setFormatter(log_format)  # 设置文件日志处理器的格式
                logger.addHandler(fh)  # 将文件日志处理器添加到日志记录器中
            except PermissionError:
                # 如果没有写入权限,则记录一条错误日志
                logger.error("无法创建日志文件,请检查权限")

        return logger  # 返回配置好的日志记录器对象


# 使用HandleLogs类配置日志记录器并命名为logs
handle: HandleLogs = HandleLogs()
logs: logging.Logger = handle.output_logs()
