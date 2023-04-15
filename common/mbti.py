"""
@Time ： 2023-04-10 20:03
@Author ：苏半夏
@File ：mbti.py
@IDE ：PyCharm
@coding: utf-8
@DESC:MBTI职业性格测试题
"""
import json


def open_json_file(filename):
    """
    :param filename: mbti.json 所在的位置
    :return: json字典
    """
    try:
        with open(filename, encoding='utf-8') as a:
            # 读取文件
            result = json.load(a)
    except Exception as e:
        print(e)
    return result


def mbti_test_instructions(result):
    """
    param: result
    desc: 打开的JSON文件
    ex：result = open_json_file(filename='../data/mbti.json')
    """
    instructions = result.get('instructions')
    print("======================测前须知=========================")
    for v in instructions.values():
        print(v)


def create_questions(result):
    """
    :param result: json字典
    :return: mbti字典
    """
    # 创建性格字典，key 为 str value为int
    mbti_demo = dict()
    mbti_demo['E'] = mbti_demo['I'] = mbti_demo['S'] = mbti_demo['N'] = 0
    mbti_demo['T'] = mbti_demo['F'] = mbti_demo['J'] = mbti_demo['P'] = 0
    # {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    questions = result.get('questions')
    for i in range(len(questions)):
        num = questions[i].get('num')
        desc = questions[i].get('desc')
        check = questions[i].get('check')
        choiceA = questions[i].get('choiceA')
        choiceB = questions[i].get('choiceB')
        # print("Q{}:{}\n{}".format(num, desc, check))
        if i <= 25:
            print("哪一个答案最能贴切的描绘你一般的感受或行为？")
            print("Q{}:{}\n{}".format(num, desc, check))
        elif 26 < i <= 57:
            print("在下列每一对词语中，哪一个词语更合你心意？请仔细想想这些词语的意义，而不要理会他们的字形或读音。")
            print("Q{}:{}".format(num, check))
        elif 58 < i <= 77:
            print("在下列每一对词语中，哪一个词语更合你心意？请仔细想想这些词语的意义，而不要理会他们的字形或读音。")
            print("Q{}:{}\n{}".format(num, desc, check))
        else:
            print("在下列每一对词语中，哪一个词语更合你心意？")
            print("Q{}:{}".format(num, check))
        input_str = input("请输入您的答案：")
        if input_str == 'A':
            for k, v in mbti_demo.items():
                if k == choiceA:
                    mbti_demo[k] = mbti_demo[k] + 1
        elif input_str == 'B':
            for k, v in mbti_demo.items():
                if k == choiceB:
                    mbti_demo[k] = mbti_demo[k] + 1
        else:
            print("请输入A或者B")
            print("循环输入功能暂未开发")
    return mbti_demo


def create_results(mbti_dict):
    """
    desc: 生成结果
    """
    if not isinstance(mbti_dict, dict):
        print("输入的类型不正确，请传递一个字典")
        return
    else:
        print("=====================系统分析中========================")
        extraversion, introversion = mbti_dict.get("E"), mbti_dict.get("I")
        sensing, intuition = mbti_dict.get("S"), mbti_dict.get("N")
        thinking, feeling = mbti_dict.get("T"), mbti_dict.get("F")
        judging, perceiving = mbti_dict.get("J"), mbti_dict.get("P")
        if introversion >= extraversion:
            result_text = "I"
        else:
            result_text = "E"
        if intuition >= sensing:
            result_text = result_text + "N"
        else:
            result_text = result_text + "S"
        if feeling >= thinking:
            result_text = result_text + "F"
        else:
            result_text = result_text + "T"
        if perceiving >= judging:
            result_text = result_text + "P"
        else:
            result_text = result_text + "J"
        return result_text


def analysis_results(text, result):
    """
    :param: text,result
    :type: str,dict
    desc: 根据传入的text，获取相应的结果描述。result 为字典
    """
    if not isinstance(result, dict):
        return
    result = result.get("result")
    for i in range(len(result)):
        for k, v in result[i].items():
            if text == result[i].get(k):
                print("你的人格是:{},是一种{}的人格".format(result[i].get("pMark"), result[i].get("called")))
                properties, territory = result[i].get("properties"), result[i].get("territory")
                profession, keyWords = result[i].get("profession"), result[i].get("keyWords")
                print("特征如下：")
                for index in range(len(properties)):
                    print("{}、{}".format(properties[index].get("descId"), properties[index].get("desc")))
                print("适合领域：{}".format(territory))
                print("适合职业：{}".format(profession))
                if "" == keyWords:
                    print("暂无关键词推荐")
                else:
                    print("推荐关键词：{}".format(keyWords))


def mbti():
    """
    主程序
    """
    filename = "../data/mbti.json"
    my_json = open_json_file(filename)
    mbti_test_instructions(my_json)
    my_mbti = create_questions(my_json)
    my_text = create_results(my_mbti)
    analysis_results(my_text, my_json)
