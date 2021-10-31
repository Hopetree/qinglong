#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Author: Hopetree <https://github.com/Hopetree>
# @Time  : 2021/10/31
# @Desc  :
# cron=10 9,18 * * *
# new Env('repo 测试1');

import os

envs = os.environ
for k, v in envs.items():
    print('{}={}'.format(k, v))
