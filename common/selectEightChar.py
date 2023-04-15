"""
@Time ： 2023-03-30 21:41
@Author ：苏半夏
@File ：selectEightChar.py
@IDE ：PyCharm
@coding: utf-8
@DESC: 查看生辰八字
本方法按照:  年柱  月柱  日柱  时柱
年柱计算方法：以立春为界限，立春之前为上一年，立春之后为本年
月柱计算方法：以节气划定月份，分为 正月建寅、二月建卯、三月建辰、四月建已、五月建午、六月建未、七月建申、八月建酉、九月建戌、十月建亥、十一月建子、十二月建丑
日柱计算方法： 按照公式：(年份 - 1900) * 5 + (年份 - 1900 + 3) / 4 + 9 + 计算日
时柱计算方法： 查表
"""
from math import floor
from common.sixtyYears import sixtyYears
from chinese_calendar import get_solar_terms
import ast
import logging
import datetime

# 调试使用下面
# logging.basicConfig(level=logging.INFO, filename="../log/selectEightChar.log")
# 正常使用
logging.basicConfig(level=logging.INFO, filename="./log/selectEightChar.log", )

tianGan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
diZhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def getLiChunDate(num):
    """
    传入年,获得立春是几月几号
    param: num  type is int    ex: 2023
    """
    temp = ""
    key = 0
    if isinstance(num, int):
        temp = get_solar_terms(datetime.date(num, 1, 1), datetime.date(num, 12, 31))
        for i in range(len(temp)):
            if '立春' in temp[i][1]:
                key = i
                break
        logging.info("{}年的立春是{}".format(num, temp[key][0]))
    else:
        logging.error("getLiChunDate 请输入正确的参数类型")
    return temp[key][0]


def judge_solar_terms(normal_date):
    """
    传入一个公历日期，判断这个日期处于什么节气之间
    """
    result = list()
    # 判断该日期是不是正值节气当天
    logging.info("判断是不是节气当天:".format(get_solar_terms(normal_date, normal_date)))
    if len(get_solar_terms(normal_date, normal_date)) > 0:
        # print("是正值当天")
        result.append(get_solar_terms(normal_date, normal_date)[0])
    else:
        # print("不是正值当天")
        # 不是正值节气当天,则取前后15天
        front_date = normal_date - datetime.timedelta(days=15)
        after_date = normal_date + datetime.timedelta(days=15)
        length = len(get_solar_terms(front_date, after_date))
        if length >= 2:
            result.append(get_solar_terms(front_date, after_date)[length - 1])
            result.append(get_solar_terms(front_date, after_date)[length - 2])
    return result


def countDay(s):
    """
    计算指定日期是当年的第几天
    param: s    type is str    ex: 20230406
    """
    y, m, d = int(s[0:4]), int(s[4:6]), int(s[6:8])
    dd = datetime.date(y, m, d)
    t = dd.strftime("%j")
    return int(t)


def getMonth(nd):
    """
    传入一个时间，判断这个时间在哪两个节气之间，根据节气返回对应的月份
    param: nd  type is datetime.date(year, month, day)
    ex: datetime.date(2023, 1, 30)
    desc:
        定义一个字典，key为月份，value为包含的节气
        判断judge_solar_terms返回的是否在value里，找对应的key，设置为month
        考虑judge_solar_terms返回为1个节气的场景
    """
    month = ""
    jieQi = {"1": "立春、雨水、惊蛰", "2": "惊蛰、春分、清明", "3": "清明、谷雨、立夏", "4": "立夏、小满、芒种",
             "5": "芒种、夏至、小暑", "6": "小暑、大暑、立秋", "7": "立秋、处暑、白露", "8": "白露、秋分、寒露",
             "9": "寒露、霜降、立冬", "10": "立冬、小雪、大雪", "11": "大雪、冬至、小寒", "12": "小寒、大寒、立春"}
    if len(judge_solar_terms(nd)) == 1:
        logging.info("当天就是节气")
        getJQ = judge_solar_terms(nd)[0][1]
        logging.info(getJQ)
        for k, v in jieQi.items():
            # 将v 转化成数组
            vList = v.split("、")
            if getJQ in v:
                if vList.index(getJQ) <= 1:
                    month = k
                else:
                    month = int(k) + 1
    elif len(judge_solar_terms(nd)) > 1:
        logging.info("在两个节气之间")
        firstJQ, lastJQ = judge_solar_terms(nd)[0][1], judge_solar_terms(nd)[1][1]
        logging.info("在{}和{}之间".format(firstJQ, lastJQ))
        for k, v in jieQi.items():
            if firstJQ in v and lastJQ in v:
                month = k

    return month


def getTwelveHour():
    """
    根据24个小时，生成地支时间
    例如：子时：23 0 1
    """
    shiZhi = dict()
    i = k = 1
    while i < 24:
        temp = list()
        if i + 1 >= 24:
            temp.append(i)
            temp.append(0)
            temp.append(1)
        else:
            temp.append(i)
            temp.append(i + 1)
            temp.append(i + 2)
        i = i + 2
        if k > 11:
            k = 0
        shiZhi[str(diZhi[k])] = str(temp)
        k = k + 1
    return shiZhi


def getChineseHour(date):
    """
    param: date
    type:  str
    ex: 13:30:37
    desc: 传入一个时间，判断该时间对应的中国时间是什么时候
    """
    m = date[:2]
    temp = getTwelveHour()
    logging.info(temp)
    result = ""
    for k, v in temp.items():
        # 将list字符串转换成list
        tempList = ast.literal_eval(v)
        try:
            if tempList.index(int(m), 0, 2) < 2:
                result = k
                break
        except Exception as e:
            logging.info(e)
    return result


def createTableCol(tg_index, dz_index):
    """
    创建日上起时表的列
    param：tgIndex and dzIndex
    type: int
    """
    temp = list()
    for num in range(12):
        if tg_index > 9:
            tg_index = 0
            temp.append(str(tianGan[tg_index] + diZhi[dz_index]))
        else:
            temp.append(str(tianGan[tg_index] + diZhi[dz_index]))
        tg_index = tg_index + 1
        dz_index = dz_index + 1
    return temp


def createDayAndHourTable():
    """
    创建日上起时表
    desc：用字典创建，日为key，value为 对应的值
    """
    table = dict()
    horIndex = ["甲己", "乙庚", "丙辛", "丁壬", "戊癸"]
    tgIndex = dzIndex = 0
    for i in range(len(horIndex)):
        temp = createTableCol(tgIndex, dzIndex)
        table[str(horIndex[i])] = str(temp)
        tgIndex = tgIndex + 2
    return table


def getEightCharOfYear(date):
    """
    param: date type: datetime.date(year, month, day)
    获取八字中的年柱
    """
    # yearText = ""
    liChunDate = getLiChunDate(date.year)
    logging.info(liChunDate)
    if liChunDate > date:
        logging.info("输入的节日是在立春之前")
        # 年柱取上一年
        index = (date.year - 1924) % 60
        yearText = sixtyYears().get(index)
    else:
        index = (date.year - 1924) % 60
        yearText = sixtyYears().get(index + 1)
        logging.info("输入的节日是在立春之后")
    return yearText


def getEightCharOfMonth(year_text, new_date):
    logging.info("year_text的值是{}".format(year_text))
    logging.info("new_date的值是{}".format(new_date))
    """
    获取生辰八字中的月柱
    """
    # tianGan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # diZhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    monthRow = {"1": "甲己", "2": "乙庚", "3": "丙辛", "4": "丁壬", "5": "戊癸"}
    monthCol = dict()
    month = getMonth(new_date)
    logging.info("month is {}".format(month))
    index = 0
    for k, v in monthRow.items():
        logging.info("v is {}".format(v))
        if year_text[0] in v:
            index = k
    tgIndex = int(index) * 2
    logging.info("tgIndex is {}".format(tgIndex))
    dzIndex = 2
    for i in range(12):
        if tgIndex > 9:
            tgIndex = 0
        if dzIndex > 11:
            dzIndex = 0
        monthCol[str(i + 1)] = tianGan[tgIndex] + diZhi[dzIndex]
        tgIndex = tgIndex + 1
        dzIndex = dzIndex + 1
    return monthCol[str(month)]


def getEightCharOfDay(date):
    logging.info("the date is {}".format(date))
    date = str(date).replace("-", "")
    """
    获取生辰八字中的日柱
    """
    # tianGan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # diZhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    # date = "20060401"
    year = int(date[0:4])
    a = (year - 1900) * 5 + (year - 1900 + 3) / 4 + 9 + countDay(date)
    return tianGan[floor(a) % 60 % 10 - 1] + diZhi[floor(a) % 60 % 12 - 1]


def getEightCharOfHour(day_text, date):
    """
    获取八字中的时柱
    """
    shi_chen = getChineseHour(date)
    table = createDayAndHourTable()
    for k, v in table.items():
        if day_text[0] in k:
            tempList = ast.literal_eval(v)
            for i in range(len(tempList)):
                if shi_chen in tempList[i]:
                    return tempList[i]


def selectEightChar(input_str):
    year = int(str(input_str.split(" ")[0]).split("/")[0])
    month = int(str(input_str.split(" ")[0]).split("/")[1])
    day = int(str(input_str.split(" ")[0]).split("/")[2])
    yearText = getEightCharOfYear(datetime.date(year, month, day))
    monthText = getEightCharOfMonth(yearText, datetime.date(year, month, day))
    dayText = getEightCharOfDay(input_str.split(" ")[0].replace("/", ""))
    hourText = getEightCharOfHour(dayText, str(input_str.split(" ")[1]))
    result = list()
    result.append(yearText)
    result.append(monthText)
    result.append(dayText)
    result.append(hourText)
    return result
