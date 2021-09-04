#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 9:15 下午
# @Author  : Xinlong Chen
# @File    : config.py

import json
import os

from .responce import Responce


def get_config() -> Responce:
    """获取验证配置"""
    config_path = os.getcwd() + os.sep + 'config.json'
    if os.path.isfile(config_path):
        try:
            with open(config_path) as config_file:
                config = json.loads(config_file.read())
            return Responce(status=0, resp=config)
        except Exception as e:
            return Responce(status=-1, msg=str(e))
    else:
        print("{} 不存在config.json文件".format(os.getcwd()))
        return Responce(status=0, msg="缺少config.json文件")
