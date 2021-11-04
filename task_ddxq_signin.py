#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
项目名称: Hopetree/qinglong
Author: Hopetree
功能：叮咚买菜签到
    0、抓包拿到叮咚买菜 cookie
    1、添加环境变量 DDXQ_COOKIE，多个用&拼接，例如 DDXQ_COOKIE=cookie1&cookie2
    2、每日签到并查询当前积分信息
Date: 2021/11/3
Update: 2021/11/4
cron: 30 8 * * *
new Env('叮咚买菜签到');
"""

import os

import requests
from common.common import send_msg, hidden_key

COOKIE = os.environ.get('DDXQ_COOKIE')
TITLE = '叮咚买菜签到'


class DDXQ:
    content_list = []

    def __init__(self, cookie):
        self.cookie = cookie
        self.hidden_ck = hidden_key(self.cookie)
        self.params = {'api_version': '9.7.3',
                       'app_version': '1.0.0',
                       'app_client_id': '3',
                       'native_version': '9.30.0',
                       'city_number': '1103',
                       'latitude': '22.602782',
                       'longitude': '113.852799'}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.30.0',
            'Cookie': self.cookie
        }

    def check_and_sign_in(self):
        """查询用户信息，查询成功就签到"""
        url = 'https://maicai.api.ddxq.mobi/user/info'
        resp = requests.get(url, headers=self.headers, params=self.params).json()
        if resp['code'] == 0:
            user_name = resp['data']['name']
            msg = self.sign_in()
            content = '用户: {}'.format(user_name) + msg
        elif resp['code'] == 9007 or resp['code'] == 1111:
            content = '\ncookie:{}\n签到失败，cookie 失效'.format(self.hidden_ck)
        else:
            content = '\ncookie:{}\n签到失败，未知错误 {}'.format(self.hidden_ck, resp)
        self.content_list.append(content)

    def query_point(self):
        """查询积分"""
        url = 'https://maicai.api.ddxq.mobi/point/home'
        resp = requests.get(url, headers=self.headers, params=self.params).json()
        point_num = resp['data']['point_num']
        point_money = resp['data']['point_money']
        expire_point_display = resp['data']['expire_point_display']
        return point_num, point_money, expire_point_display

    def sign_in(self):
        """签到"""
        url = 'https://sunquan.api.ddxq.mobi/api/v2/user/signin/'
        resp = requests.post(url, headers=self.headers, json=self.params).json()
        if resp['code'] == 0:
            sign_series = resp['data']['sign_series']
            point_num, point_money, expire_point_display = self.query_point()
            msg = '\n签到成功，获得积分：{}\n总积分：{}\n积分价值：{}元\n积分过期：{}'.format(
                sign_series, point_num,
                point_money,
                expire_point_display)
        else:
            msg = '\ncookie:{}\n签到失败 {}'.format(self.hidden_ck, resp)
        return msg


def main():
    if COOKIE:
        cookie_list = COOKIE.strip().split('&')
        for ck in cookie_list:
            xq = DDXQ(ck)
            xq.check_and_sign_in()
        send_msg(TITLE, '\n'.join(DDXQ.content_list))
    else:
        print('没有设置环境变量 DDXQ_COOKIE，无法签到')


if __name__ == '__main__':
    main()
