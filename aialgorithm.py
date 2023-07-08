# coding: utf8
import sys
import random
import math
import copy
from flask import request
import numpy as np
from dataaccess import DataAccess

POINTS_SIZE = 0         # 都市数(個体の遺伝子数)
POPULATION_SIZE = 10    # 集団の個体数
GENERATION = 10         # 世代数
MUTATE = 0.1            # 突然変異の確率
SELECT_RATE = 0.5       # 選択割合

# 経路(個体)の距離(適応度)を計算する
def calc_distance(points, route):
    distance = 0
    for i in range(POINTS_SIZE):
        (x0, y0) = points[route[i]]
        if i == POINTS_SIZE - 1:
            (x1, y1) = points[route[0]]    
        else:
            (x1, y1) = points[route[i+1]]
        # distance = distance + math.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))
        distance = distance + gis_distance(x0, y0, x1, y1)
    return distance
    
# 集団を距離(適応度)で昇順にソートする
def sort_fitness(points, population):
    fp = []
    for individual in population:
        fitness = calc_distance(points, individual)
        fp.append((fitness, individual))
    fp.sort()

    sorted_population = []    
    
    for fitness, individual in fp:
        sorted_population.append(individual)
        
    return sorted_population

# 選択: 適応度の高い(距離が短い)個体を残す
def selection(points, population):
    sorted_population = sort_fitness(points, population)
    n = int(POPULATION_SIZE * SELECT_RATE)    
    
    return sorted_population[0:n]

# 交叉: 交叉点の範囲（r1～r2）は乱数で決める
def crossover(ind1, ind2):

    r1 = random.randint(0, POINTS_SIZE - 1)
    r2 = random.randint(r1 + 1, POINTS_SIZE)

    flag = [0] * POINTS_SIZE
    ind = [-1] * POINTS_SIZE

    for i in range(r1, r2):
        city = ind2[i]
        ind[i] = city
        flag[city] = 1
    
    for i in list(range(0, r1)) + list(range(r2, POINTS_SIZE)):
        city = ind1[i]
        if flag[city] == 0:
            ind[i] = city
            flag[city] = 1
            
    for i in range(0, POINTS_SIZE):
        if ind[i] == -1:
            for j in range(0, POINTS_SIZE):
                city = ind1[j]
                if flag[city] == 0:
                    ind[i] = city
                    flag[city] = 1
                    break
    return ind

# 突然変異: 個体の各遺伝子に対して突然変異確率(MUTATE)に従って突然変異させる
def mutation(ind1):
    ind2 = copy.deepcopy(ind1)
    if random.random() < MUTATE:
        city1 = random.randint(0, POINTS_SIZE - 1)
        city2 = random.randint(0, POINTS_SIZE - 1)
        if city1 > city2:
            city1, city2 = city2, city1
        ind2[city1:city2+1] = reversed(ind1[city1:city2+1])
    return ind2

def gis_distance(lat1, lng1, lat2, lng2):
    R = 6378.137
    x1 = R * math.cos(math.pi * lat1 / 180) * math.cos(math.pi * lng1 / 180)
    y1 = R * math.cos(math.pi * lat1 / 180) * math.sin(math.pi * lng1 / 180)
    z1 = R * math.sin(math.pi * lat1 / 180)
    x2 = R * math.cos(math.pi * lat2 / 180) * math.cos(math.pi * lng2 / 180)
    y2 = R * math.cos(math.pi * lat2 / 180) * math.sin(math.pi * lng2 / 180)
    z2 = R * math.sin(math.pi * lat2 / 180)
    d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return 2 * R * math.asin( d / 2 / R )

def ga(spot_list):

    out = []

    # points = []
    # for i in range(POINTS_SIZE):
    #     points.append((random.random(), random.random()))
    # print(points)

    points = []
    for spot in spot_list:
        points.append((float(spot[0]), float(spot[1])))
    out.append(points)

    # 初期集団を生成
    # 各都市を一巡する経路の集団
    population = []
    for i in range(POPULATION_SIZE):
        # 個体（経路）
        individual = list(range(POINTS_SIZE))
        # 経路をランダムに入れ替える
        random.shuffle(individual)
        population.append(individual)

    # 都市の座標を表示
    out.append(population)
    
    # GAの開始
    for generation in range(GENERATION):
        out.append(u"tsp_ga (" + str(generation + 1) + u"generation)")
        
        # 選択
        population = selection(points, population)
        
        # 交叉して増やす個体数
        n = POPULATION_SIZE - len(population)
        for i in range(n):
            # 集団から2個体をランダムに選び、
            # 交叉した個体を生成する
            r1 = random.randint(0, len(population) - 1)
            r2 = random.randint(0, len(population) - 1)
            individual = crossover(population[r1], population[r2])
    
            # 突然変異させる
            individual = mutation(individual)
    
            # 集団に追加する
            population.append(individual)
    
        # 集団を適応度順にソートする
        sort_fitness(points, population)
        
        # 都市の経路を描画
        for ind in range(POPULATION_SIZE):
            route = population[ind]
            dist = calc_distance(points, route)
            
            out.append((route, dist))
            
            for i in range(POINTS_SIZE):
                (x0, y0) = points[route[i]]
                if i == POINTS_SIZE - 1:
                    (x1, y1) = points[route[0]]
                else:
                    (x1, y1) = points[route[i+1]]
    a = out[106][0]
    return a

#感性的特徴で観光地を探す
##ベクトル内積、類似度計算
def query():
    da = DataAccess()
    data = da.get_spots()
    query = []
    target = []
    result = []
    for i in ["history_culture","food_product","nature","view","experience"]:
        query.append(request.form[i])
    for d in data:
        target.extend([d[5], d[6], d[7], d[8], d[9]])
    query = np.array(query, dtype=int).reshape(-1,1)
    target = np.array(target, dtype=int).reshape(-1,5)
    sim = np.dot(target, query)
    result.extend([np.where(sim == sim.max())])
    return result[0][0]

# main関数
# if __name__ == '__main__':

#     spot_list = [
#         ['35.6802117', '139.7576692'],
#         ['35.6809591', '139.7673068'],
#         ['35.7100069', '139.8108103'],
#         ['35.658584', '139.7454316'],
#         ['35.6313051', '139.7777839'],
#         ['35.7001058', '139.5754574']
#     ]

#     POINTS_SIZE = len(spot_list)

#     ga(spot_list)
