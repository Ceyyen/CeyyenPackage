"""
@Time ： 2023-03-29 21:54
@Author ：苏半夏
@File ：ThirtySecondTest.py
@IDE ：PyCharm
@coding: utf-8
@DESC: 30s 看出你内心的生活
"""


def thirtySecondTest():
    """
    :return: null
    desc:   30s 看出你内心的生活
    """
    mydict = dict()
    print("现有1-11,一共11位数字")
    print("1 2 3 4 5 6 7 8 9 10 11")
    nums = input("请输入任意两个数字(空格区分)，放在1和2旁边\n")
    mydict["1"] = nums.split(" ")[0]
    mydict["2"] = nums.split(" ")[1]
    print("请输入任意两个异性的名字，放在3和7旁边")
    firstName = input("请输入数字3对应的异性名字\n")
    secName = input("请输入数字7对应的异性名字\n")
    mydict["3"], mydict["7"] = firstName, secName
    print("请输入任意三个朋友或亲戚的名字，放在4、5、6旁边")
    faffName = input("请输入数字4对应的朋友或亲戚名字\n")
    fafsName = input("请输入数字5对应的朋友或亲戚名字\n")
    faftName = input("请输入数字6对应的朋友或亲戚名字\n")
    mydict["4"], mydict["5"], mydict["6"] = faffName, fafsName, faftName
    print("请输入任意四首歌曲的名字，放在8、9、10、11旁边")
    firstSong = input("请输入数字8对应的歌曲名字\n")
    secSong = input("请输入数字9对应的歌曲名字\n")
    thSong = input("请输入数字10对应的歌曲名字\n")
    fourthSong = input("请输入数字11对应的歌曲名字\n")
    mydict["8"], mydict["9"], mydict["10"], mydict["11"] = firstSong, secSong, thSong, fourthSong
    print("==========================================")
    print("您现在的数字情况如下：")
    for k, v in mydict.items():
        print("数字{}对应的是{}".format(k, v))
    print("""把想法告诉{}，{}是你爱的人，{}是你喜欢，却不能在一起的人。\n{}是你最关心的人，{}是非常了解你的人，{}是你最重要的人。
 """.format(mydict["5"], mydict["3"], mydict["7"], mydict["4"], mydict["5"], mydict["6"]))
    print("""{}适合歌曲《{}》,{}适合歌曲《{}》,\n歌曲《{}》代表你的想法,歌曲《{}》代表你的生活感受。
    """.format(mydict["8"], mydict["3"], mydict["9"], mydict["7"], mydict["10"], mydict["11"]))
