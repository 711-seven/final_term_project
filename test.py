为猜数字游戏增加记录玩家成绩的功能，包括玩家用户名、玩的次数和平均猜中的轮数等；
如果记录里没有玩家输入的用户名，就新建一条记录，否则在原有记录上更新数据；
对玩家输入做检测，判定输入的有效性，并保证程序不会因异常输入而出错；
从网络上获取每一局的答案，请求地址：https://python666.cn/cls/number/guess/

import pandas as pd
import requests


def load_record(name, info):    # 从读取的文件中获得历史记录

    if name in info.index:
        games = info.loc[name, "number_of_games"]
        min_rounds = info.loc[name, "min_rounds_per_game"]
        avg_rounds = info.loc[name, "avg_rounds_per_game"]
    else:
        games = 0
        min_rounds = 0
        avg_rounds = 0

    print("%s，你已经玩了%d次，最少%d轮猜出答案，平均%.2f轮猜出答案，"
          "开始游戏！" %(name, games, min_rounds, avg_rounds ))

    return games, min_rounds, avg_rounds


def guess_num():   # 判断数据有效性 + 一次猜大小
    r = requests.get("https://python666.cn/cls/number/guess")
    answer = int(r.text)
    rounds = 0
    guess = 0

    while guess != answer:
        input_ = input("请猜一个1-100的数字：")
        rounds += 1
        while input_ or input_ == '':
            try:
                guess = int(input_)
                if guess < 1 or guess > 100:
                    input_ = input("输入有误，请重新输入一个1-100的数字：")
                else:
                    break
            except Exception:
                input_ = input("输入有误，请重新输入一个1-100的数字：")

        if guess < answer:
            print("猜小了，再试试")
        elif guess > answer:
            print("猜大了，再试试")

    print("猜对了，你一共猜了%d轮" %rounds)
    return rounds


with open("user_info.csv", "r", encoding='utf-8') as f:     # 读取文件
    df = pd.read_csv(f, sep=",")
    print(df)
    data = df.set_index("user_name")

n = input("请输入你的名字：")
g, min_r, avg_r = load_record(n, data)          # 获取历史记录并返回值
ttl_r = g * avg_r
flag = True

while flag:
    g += 1
    r = guess_num()                          # 进行一次猜数字并返回round次数
    ttl_r += r
    if r < min_r or min_r == 0:
        min_r = r
    else:
        pass
    avg_r = ttl_r / g

    print("%s，你已经玩了%d次，最少%d轮猜出答案，平均%.2f轮猜出答案，"
          % (n, g, min_r, avg_r))
    str = input("是否继续游戏？（输入y继续，其他退出）")
    if str != "y":
        flag = False
    else:
        pass

# 若原df中没有这条，则添加一行；若有，则修改改行
data.loc[n] = {"number_of_games": g,
               "min_rounds_per_game": min_r,
               "avg_rounds_per_game": avg_r}

# 新的df覆盖原csv文件中的内容
data.to_csv("user_info.csv", sep=",", encoding="utf-8")

# 验证数据是否成功写入
with open ("user_info.csv", "r", encoding="utf-8") as f:
    df_1 = pd.read_csv(f, sep=",")
print(df_1)






