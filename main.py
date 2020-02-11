import math


# 读取文件
def ReadFile(ratings):
    """
    :param ratings: 用户评分文件
    :return:
    """
    user_rating = dict()
    with open(ratings, "r", encoding="utf-8") as fp:
        for line in fp:
            user, item, score = line.split(",")[0:3]  # 切片左闭右开
            # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
            user_rating.setdefault(user, {})
            user_rating.get(user)[int(item)] = float(eval(score))
    return user_rating


# 用户-物品倒排表（共现矩阵）
def ItemSimilarity(train):
    """
    :param train: 数据集
    :return: 将共现矩阵C归一化的物品之间的余弦相似度矩阵W
    """
    C = dict()  # 共现矩阵
    N = dict()  # 物品各自出现的总次数
    for user, items in train.items():
        for i in items.keys():
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in items:
                if i == j:
                    continue
                else:
                    C[i].setdefault(j, 0)
                    C[i][j] += 1  # 同时喜欢i，j的用户数
    W = dict()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W.setdefault(i, {})
            W[i].setdefault(j, 0)
            W[i][j] = cij / math.sqrt(N[i] * N[i])
    return W


# 生成推荐列表
def Recommendation(train, user_id, W, K):
    """
    :param train: 数据
    :param user_id: 用户id
    :param W: 共现矩阵
    :param K: 推荐的数量
    :return:
    """
    rank = dict()
    ru = train[user_id]  # 指定用户的评分
    for i, pi in ru.items():
        for j, wj in sorted(W[i].items(), key=lambda x: x[1], reverse=True)[0:K]:
            if j in ru:
                continue
            rank.setdefault(j, 0)
            rank[j] += pi * wj
    return rank


# 主模块
def start(ratings, userId, top=5):
    """
    :param ratings: 用户评分文件
    :param userId: 指定用户的id
    :param top: 推荐的数量，默认为5
    :return:
    """
    users_rating = ReadFile(ratings)
    W = ItemSimilarity(users_rating)
    result = Recommendation(users_rating, userId, W, top)
    print(result)


start('data.csv', '3')
