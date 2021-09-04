#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 10:17 下午
# @Author  : Xinlong Chen
# @File    : __main__.py

import os
import sys

from absl import app

sys.path.append('.')
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from Bilibili_Live_Spider.live_spider import main

app.run(main)
