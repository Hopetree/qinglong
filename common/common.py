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
    """
    调用青龙或者jd签到的发送信息脚本推送消息
    :param title: 信息标题
    :param content: 信息内容
    :return:
    """
    print("【{}】\n{}".format(title, content))
    try:
        if os.path.isfile(os.path.join(root_path, 'notify.py')):
            from notify import send
        elif os.path.isfile(os.path.join(root_path, 'sendNotify.py')):
            from sendNotify import send
        send(title, content)
    except ModuleNotFoundError:
        print('[通知功能]：无法获取消息通知脚本，不发送消息')
    except Exception as e:
        print('[通知功能]：其他错误：%s' % e)


def hidden_key(key):
    """
    隐藏信息，将一个字符串的中间部分替换成*
    :param key:
    :return:
    """
    long = len(key)
    if long < 3:
        return key
    else:
        cut_num = long // 3
        return key[0:cut_num] + '***' + key[0 - cut_num:]


if __name__ == '__main__':
    send_msg('title', 'content')
    print(hidden_key('24142441uuuyy'))
