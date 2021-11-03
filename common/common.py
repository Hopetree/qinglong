#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
提供一些通用的方法和类
"""

import os
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)


def send_msg(title, content):
    print("【{}】: {}".format(title, content))
    try:
        from sendNotify import send
        send(title, content)
    except ModuleNotFoundError:
        print('[通知功能]：无法获取消息通知脚本，不发送消息')
    except Exception as e:
        print('[通知功能]：其他错误：%s' % e)


if __name__ == '__main__':
    send_msg('title', 'content')
