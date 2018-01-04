# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 20:44
# @Author  : Mocha Lee
# @Email   : 1446684220@qq.com
# @File    : 1.py
# @Software: PyCharm Community Edition


import requests
import json

session = requests.session()
APPID = 'wx7a727ff7d940bb3f'


def get_packet():
    '''该函数用来获取小程序包'''
    headers = {
        'Accept-Encoding': 'gzip',
        'User-Agent': 'MicroMessenger Client',
        'Content-Type': 'application/octet-stream',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '*/*',
    }
    req = session.get(
        'https://res.servicewechat.com/weapp/release/wx7a727ff7d940bb3f/14.wxapkg?rand=1192033587&pass_key=UfkTXX5U0A-gr6mad_49Evw8qNKn9vNZCNIoPclz0VuHT6w6Cx8U_rbKQCUU-41O9vy2dqBGFn1I0-ydGEgYcEhWR02MgE9OK8CdDP1jiA43dCEhZnPTH5tAiW1AbN2E&ext_code=hQfMJjqOYIY0fk6CDERUQCZm2DNaZJe9Nf4nNrWu-Dg',
        headers=headers
    )
    with open('wx7a727ff7d940bb3f.wxapkg', 'wb+') as f:
        f.write(req.content)


def get_sig(score_list):
    score_with_salt = APPID
    for item in score_list:
        score_with_salt += '_' + str(item.get('key', '')) + ':' + str(item.get('value', ''))

    print('score_with_salt: {}'.format(score_with_salt))
    result = 0
    for index, ch in enumerate(score_with_salt):
        result = 31 * result + ord(ch)
    result &= 67108863
    print('result: {}'.format(result))
    return result


def main():
    sessionid = input('please input sessionid:')
    headers = {
        'charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        'referer': 'https://servicewechat.com/wx7a727ff7d940bb3f/14/page-frame.html',
        'content-type': 'application/json',
        'User-Agent': 'MicroMessenger/6.6.1.1220(0x26060133) NetType/WIFI Language/zh_CN'
    }
    # score_list = [{"key":"newscore","value":1800},{"key":"level","value":109},{"key":"baoshi","value":0},{"key":"combo","value":8}]
    score_list = [
        {"key": "newscore", "value": 232800},
        {"key": "level", "value": 334},
        {"key": "baoshi", "value": 233},
        {"key": "combo", "value": 233}
    ]
    data = {
        "appid": APPID,
        "game_behav_list": score_list,
        "sync_type": 1,
        "sig": get_sig(score_list),
        "use_time": 120
    }
    req = session.post(
        'https://game.weixin.qq.com/cgi-bin/gametetrisws/syncgame?session_id={}'.format(sessionid),
        data=json.dumps(data),
        headers = headers
    ).json()
    print(req)
    if req.get('errcode', -1) == 0:
        print('success!')
    else:
        print('sorry, some error happend! please contact the author.')


if __name__ == '__main__':
    main()
