#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys

import requests

import time
import hashlib
import base64
import hmac
import calendar


def gen_sign(timestamp, secret):
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


JOB_URL = sys.argv[1]
JOB_NAME = sys.argv[2]
BUILD_NUMBER = sys.argv[3]
BUILD_USER = sys.argv[4]
isFinish = "开始构建" if str(sys.argv[5]) == str(0) else "构建完成"
timestamp = str(calendar.timegm(time.gmtime()))
currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sign_key = 'E7ZmCwfZPsFLVsuMXKpQRf'
sgin = gen_sign(timestamp, sign_key)
url = 'https://open.feishu.cn/open-apis/bot/v2/hook/612e56d6-c06c-47d3-9bd6-4ef70c311970'
method = 'post'
headers = {
    'Content-Type': 'application/json'
}
json = {
    "timestamp": "" + timestamp + "",
    "msg_type": "interactive",
    "sign": "" + sgin + "",
    "card": {
        "config": {
            "wide_screen_mode": True,
            "enable_forward": True
        },
        "elements": [
            {
            "tag": "div",
            "text": {
                "content": "项目名称：" + JOB_NAME + "\n构建编号：第" + BUILD_NUMBER + "次\n构建运行时间：" + currenttime+"\n构建人："+ BUILD_USER+"\n<at id=all></at>",
                "tag": "lark_md"
            }
        }, {
            "actions": [{
                "tag": "button",
                "text": {
                    "content": "查看报告",
                    "tag": "lark_md"
                },
                "url": JOB_URL,
                "type": "default",
                "value": {}
            }],
            "tag": "action"
        }],
        "header": {
            "title": {
                "content": JOB_NAME + " "+isFinish+"",
                "tag": "plain_text"
            }
        }
    }
}
requests.request(method=method, url=url, headers=headers, json=json)

