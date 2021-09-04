#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 9:19 下午
# @Author  : Xinlong Chen
# @File    : responce.py

class Responce:
    def __init__(self, status=0, msg="OK", resp=None):
        self.status = status
        self.msg = msg
        self.resp = resp
