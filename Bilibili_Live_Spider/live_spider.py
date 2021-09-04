#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 9:09 下午
# @Author  : Xinlong Chen
# @File    : live_spider.py

import random
import re
import sys
import time

import browsercookie
import requests

from .Utils.config import get_config


def get_token(config, cookies_jar):
    # get token, this is a part of cookie
    # if not login, wouldn't get it!
    # please login in web page!
    for cookie in cookies_jar:
        if cookie.name == "bili_jct" and cookie.domain == ".bilibili.com":
            config['token'] = cookie.value
    if not config.__contains__('token'):
        print("请先在浏览器上登陆BiliBili！")
        sys.exit(0)


def get_room_id(config: dict, cookies_jar):
    # get room_id from url
    # each url have it's room_id
    # can't use last part of url as room_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'refer': 'https://live.bilibili.com/'
    }

    resp = requests.get(config['url'], cookies=cookies_jar, headers=headers).text
    if re.search(r'room_id":(.*?),', resp):
        roomid_list = re.findall(r'room_id":(.*?),', resp)
        for iter in roomid_list:
            if int(iter) != 0:
                config['room_id'] = iter
                break
    else:
        print("该直播间不存在或主播已经下播！")
        sys.exit(0)
    if not config.__contains__('room_id'):
        print("该直播间不存在或主播已经下播！")
        sys.exit(0)


def get_barrage(config):
    url = 'https://api.live.bilibili.com/ajax/msg'
    data = {
        'roomid': config['room_id'],
        'csrf_token': config['token']
    }

    html = requests.post(url, data=data)
    result = html.json()['data']['room']
    return [tmp['text'] for tmp in result]


def send_barrahe(config, cookies_jar, msg):
    url = 'https://api.live.bilibili.com/msg/send'
    data = {
        'color': '16777215',
        'fontsize': '25',
        'mode': '1',
        'msg': msg,
        'rnd': int(time.time()),
        'roomid': config['room_id'],
        'csrf_token': config['token'],
        'csrf': config['token']
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'refer': 'https://live.bilibili.com/'
    }
    try:
        send_resp = requests.post(url, cookies=cookies_jar, headers=headers, data=data)
        result = send_resp.json()
        if result['code'] != 0:
            print(" 弹幕发送失败 :'{}' {}".format(msg, result['msg']))
        else:
            print(" 弹幕发送成功 :'{}' {}".format(msg, result['msg']))
    except Exception as e:
        print(" 弹幕发送失败 :'{}' {}".format(msg, repr(e)))


def main(self):
    # get config from config.json
    config_resp = get_config()
    if config_resp.status != 0:
        print(config_resp.msg)
        sys.exit(0)
    config = config_resp.resp

    # if input url, write cover it
    try:
        config['url'] = sys.argv[1]
    except IndexError:
        pass
    print(config)
    # find cookie from browser
    cookies_jar = browsercookie.load()

    # get token, and set it into config
    get_token(config, cookies_jar)

    # get room_id, and set it into config
    get_room_id(config, cookies_jar)

    while True:
        # get some barrages from the live
        barrages = get_barrage(config)
        # random choice a barrage
        send_msg = random.choice(barrages)
        # send it
        send_barrahe(config, cookies_jar, send_msg)
        # sleep some time
        print("{} sleep {}".format('*' * 10, '*' * 10))
        time.sleep(config['sleep_time'])
