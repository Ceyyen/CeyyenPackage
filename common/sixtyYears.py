"""
@Time ： 2023-03-27 21:11
@Author ：苏半夏
@File ：sixtyYears.py
@IDE ：PyCharm
@coding: utf-8
@DESC:60甲子
"""
import copy
from datetime import datetime
from zhdate import ZhDate

tianGan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
diZhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
Numerology = ["海中金", "炉中火", "大林木", "路旁土", "剑锋金", "山头火", "涧下水", "城头土", "白蜡金", "杨柳木", "泉中水", "屋上土", "霹雳火", "松柏木", "长流水",
              "砂石金", "山下火", "平地木", "壁上土", "金箔金", "灯头火", "天河水", "大驿土", "钗钏金", "桑柘木", "大溪水", "沙中土", "天上火", "石榴木", "大海水"]


def sixtyYears():
    tiangannew = copy.deepcopy(tianGan)
    for i in range(5):
        tiangannew.extend(tianGan)
    dizhinew = copy.deepcopy(diZhi)
    for i in range(4):
        dizhinew.extend(diZhi)
    yearList = dict()
    for i in range(60):
        yearList[i + 1] = tiangannew[i] + dizhinew[i]
    return yearList


def naYinFiveElement():
    nFE = dict()
    for k, v in sixtyYears().items():
        temp = (k - 1) // 2
        nFE[v] = Numerology[temp]
    return nFE


def mainProcess(date):
    """
    :param date: 主程序
    :return:
    """
    year, month, day = int(date[0:4]), int(date[4:6]), int(date[6:])
    myDate = datetime(year, month, day)
    date2 = ZhDate.from_datetime(myDate)
    # 1924年是甲子年 1984年
    index = (date2.lunar_year - 1924) % 60 + 1
    result = naYinFiveElement().get(sixtyYears().get(index))
    return result
