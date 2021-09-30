#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author@Haris Wang
import pytz
import json
import requests
from time import sleep,time
from random import randint
from datetime import datetime

s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;  AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045136 Mobile Safari/537.36 wxwork/3.0.16 MicroMessenger/7.0.1 NetType/WIFI Language/zh",}
s.headers.update(header)

api_key = ""
#api_key = "SCU100053Td2d54d8e5bd9adb34ac271affaa501195ed3c5d763406"

m_content = []

def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
    requests.get(msg_url)


def login(s: requests.Session, username, password):
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://wfw.scu.edu.cn/a_scu/api/sso/check", data=payload)
    if r.json().get('m') != "操作成功":
        return 0
    return 1


def get_daily(s: requests.Session):
    daily = s.get("https://wfw.scu.edu.cn/ncov/api/default/daily?xgh=0&app_id=scu")
    # info = s.get("https://app.ucas.ac.cn/ncov/api/default/index?xgh=0&app_id=ucas")
    j = daily.json()
    d = j.get('d', None)
    if d:
        return daily.json()['d']
    else:
        print("获取昨日信息失败")


def submit(s: requests.Session, old: dict):
    new_daily = {
        "sfjzxgym": old["sfjzxgym"],
        "jzxgymrq": old["jzxgymrq"],
        "sfjzdezxgym": old["sfjzdezxgym"],
        "jzdezxgymrq": old["jzdezxgymrq"],
        "qksm": old["qksm"],
        "remark": old["remark"],
        "gllx": old["gllx"],
        "glksrq": old["glksrq"],
        "jcbhlx": old["jcbhlx"],
        "jcbhrq": old["jcbhrq"],
        "bztcyy": old["bztcyy"],
        "szcs": old["szcs"],
        "szgj": old["szgj"],
        "jcjg": old["jcjg"],
        "jcqzrq": old["jcqzrq"],
        "sfjcqz": old["sfjcqz"],
        "sfjxhsjc": old['sfjxhsjc'],    #是否进行核酸检查 1
        'hsjcjg': old['hsjcjg'],        #核算检测结果 2
        "hsjcrq": "2020-09-11",
        "hsjcdd": "四川大学华西医院",
        "szxqmc": "江安校区",
        'tw': old['tw'],                #体温 3
        'sfcxtz': old['sfcxtz'],        #是否出现体征？ 4
        'sfjcbh': old['sfjcbh'],        #是否接触病患 ？疑似/确诊人群 5
        'sfcxzysx': old['sfcxzysx'],    #是否出现值得注意的情况？ 6
        'sfyyjc': old['sfyyjc'], #是否医院检查？ 7
        'jcjgqr': old['jcjgqr'], #检查结果确认？ 8
        'address': old['address'], # 9
        'geo_api_info': '{"type":"complete","position":{"Q":30.556680501303,"R":103.991700846355,"lng":103.991701,"lat":30.556681},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":40,"isConverted":true,"status":1,"addressComponent":{"citycode":"028","adcode":"510116","businessAreas":[{"name":"白家","id":"510116","location":{"Q":30.562482,"R":104.006821,"lng":104.006821,"lat":30.562482}}],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"长城路二段","streetNumber":"187号","country":"中国","province":"四川省","city":"成都市","district":"双流区","township":"西航港街道"},"formattedAddress":"四川省成都市双流区西航港街道励行西 路四川大学江安校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}', # 10
        'area': old['area'], # 11
        'province': old['province'], # 12
        'city': old['city'], # 13
        'sfzx': old['sfzx'],            #是否在校 14
        'sfjcwhry': old['sfjcwhry'],    #是否接触武汉人员 15
        'sfjchbry': old['sfjchbry'],    #是否接触湖北人员 16
        'sfcyglq': old['sfcyglq'],      #是否处于隔离期？ 17
        'sftjhb': old['sftjhb'],        #是否途经湖北 18
        'sftjwh': old['sftjwh'],        #是否途经武汉 19
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y%m%d"), # 20
        'uid': old['uid'],
        'created': str(int(time())),  # 创建时间
        'szsqsfybl': old['szsqsfybl'],  # 21
        'sfsqhzjkk': old['sfsqhzjkk'],  # 22
        'sfygtjzzfj': old['sfygtjzzfj'],# 23
        'ismoved': old['ismoved'],      #？所在地点 24
            'zgfxdq': old['zgfxdq'],
            'mjry': old['mjry'],
            'csmjry': old['csmjry'],
        "created_uid": old["created_uid"]
        }
    r = s.post("https://wfw.scu.edu.cn/ncov/wap/default/save", data=new_daily)
    print("提交信息:", new_daily)
    result = r.json().get("m")
    return result

    if result == "操作成功":
        print("打卡成功")
        if api_key:
            message(api_key, result, new_daily)
    else:
        print("打卡失败，错误信息: ", result)
        if api_key:
            message(api_key, result, new_daily)


def make_post(user, passwd):
    rc = login(s, user, passwd)
    if rc != 1:
      m_content.append(str(user) + " " + "登录失败")
      return rc
    yesterday = get_daily(s)
    res = submit(s, yesterday)
    m_content.append(str(user) + " " + res)
    return 1



print("---------------Here it is")


data = []

with open("login.json", "r") as f:
        data = json.load(f)

for item in data:
        make_post(item["u"], item["p"])

strcont = ""
for item in m_content:
    strcont += item+"    \n"

#print(strcont)

if api_key:
	message(api_key, "今日健康打卡情况", strcont)
