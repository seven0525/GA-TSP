# coding: utf8
import sys
import random
import math
import copy
import tkinter

# パラメーター
SCREEN_WIDTH  = 150
SCREEN_HEIGHT = 150
POINTS_SIZE = 50 # 都市の数
POPULATION_SIZE = 20 #集団の個体数
GENERATION = 2000 # 世代数
MUTATE = 0.3 #突然変異の確率
SELECT_RATE = 0.5 #選択割合

# 経路の距離を計算する
def calc_distance(points, route):
    distance = 0
    for i in range(POINTS_SIZE):
        (x0, y0) = points[route[i]]
        # 最後は始点に戻る
        if i == POINTS_SIZE - 1:
            (x1, y1) = points[route[0]]
        else:
            (x1, y1) = points[route[i + 1]]
        # 2点の距離を求める
        distance = distance + math.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))
    return distance


# 集団を距離（適応度）で昇順にソートする
def sort_fitness(points, population):
    fp = []
    for individual in population:
        fitness = calc_distance(points, individual)
        fp.append((fitness, individual))
    fp.sort()  # 適応度でソート（昇順）

    sorted_population = []
    # リストに入れ直す
    for fitness,  individual in fp:
        sorted_population.append(individual)
    return sorted_population

# 選択
def selection(points, population):
    sorted_population = sort_fitness(points, population)
    n = int(POPULATION_SIZE * SELECT_RATE)
    return sorted_population[0 : n]


# 交叉（ランダムな範囲をr1,r2に置き換える）
def crossover(ind1, ind2):
    r1 = random.randint(0, POINTS_SIZE -1)
    r2 = random.randint(r1 + 1, POINTS_SIZE)
    
    # 使った年のフラグのリストを0で初期化
    flag = [0] *  POINTS_SIZE
    # 子の個体（-1で初期化）
    ind = [-1] * POINTS_SIZE
    
    # r1-r2をind2から複製
    for i in range(r1, r2):
        city = ind2[i]
        ind[i] = city
        flag[city] = 1 # 使った都市のフラグに1をセット
        
        # 残り範囲はまだ使われていない遺伝子をind1から継承
        for i in list(range(0, r1)) + list(range(r2, POINTS_SIZE)):
            city = ind1[i]
            # その都市が使われていない場合
            if flag[city] == 0:
                ind[i] = city
                flag[city] = 1
            
        # 残った都市はまだ使われていない遺伝子をランダムで当てはめる
        for i in range(0, POINTS_SIZE):
            if ind[i] == -1:
                for j in range(0, POINTS_SIZE):
                    city = ind1[j]
                    if flag[city] == 0:
                        ind[i] = city
                        flag[city] = 1
                        break
        return ind


# 突然変異（ランダムに円乱打都市１と都市２の間を逆順にする）
def mutation(ind1):
    ind2 = copy.deepcopy(ind1)
    if random.random() < MUTATE:
        # 都市1
        city1 = random.randint(0, POINTS_SIZE - 1)
        # 都市2
        city2 = random.randint(0, POINTS_SIZE - 1)
        if city1 > city2:
            city1, city2  = city2, city1 # 入れ替え
        ind2[city1:city2+1] = reversed(ind1[city1:city2+1])
    return ind2

# メイン処理
# ウィンドウ初期化
root = tkinter.Tk()
root.title("TSPをGAで解いてみる")

width_size = 5 # 横方向の配置数
height_size = math.ceil(POPULATION_SIZE / width_size) # 縦方向の配置数
window_width = SCREEN_WIDTH * width_size # ウィンドウの幅
window_height = SCREEN_HEIGHT * height_size # ウィンドウの高さ
root.geometry(str(window_width) + "x" + str(window_height)) # ウィンドウのサイズ

canvas_list = []
for i in range(POPULATION_SIZE):
    canvas = tkinter.Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    cx = i % width_size * SCREEN_WIDTH
    cy = int(i / width_size) * SCREEN_HEIGHT
    canvas.place(x = cx, y = cy)
    canvas_list.append(canvas)

# 都市の座標を生成
points = []
for i in range(POINTS_SIZE):
    points.append((random.random(), random.random()))

# 各都市を一巡する経路の初期集団の生成
population = []
for i in range(POPULATION_SIZE):
    # 個体(経路)
    individual = list(range(POINTS_SIZE))
    # 経路をランダムに入れ替える
    random.shuffle(individual)
    population.append(individual)
    
for generation in range(GENERATION):
    root.title(u"TSPをGAで解いてみる（" + str(generation +  1) + u"世代）")
    
    # 選択
    population = selection(points, population)
    
    # 交叉と突然変異
    # 交叉して増やす個体数
    n = POPULATION_SIZE - len(population)
    for i in range(n):
        r1 = random.randint(0, len(population) -1)
        r2 = random.randint(0, len(population) -1)
        individual = crossover(population[r1], population[r2])
        
        #突然変異させて集団に追加
        individual = mutation(individual)
        population.append(individual)
        
    sort_fitness(points, population) # 適応度順にソート
    
    # 都市の経路を描画
    for ind in range(POPULATION_SIZE):
        canvas = canvas_list[ind]
        route = population[ind]
        dist = calc_distance(points, route)
        canvas.delete('all')
        for i in range(POINTS_SIZE):
            (x0, y0) = points[route[i]]
            if i == POINTS_SIZE - 1:
                (x1, y1) = points[route[0]]
            else:
                (x1, y1) = points[route[i + 1]]
            
            canvas.create_line(
                x0 * SCREEN_WIDTH, 
                y0 * SCREEN_HEIGHT,
                x1 * SCREEN_WIDTH, 
                y1 * SCREEN_HEIGHT, 
                fill="black",
                width=1)
            canvas.create_oval(
                x0 * SCREEN_WIDTH - 2,
                y0 * SCREEN_HEIGHT - 2,
                x0 * SCREEN_WIDTH + 2,
                y0 * SCREEN_HEIGHT + 2,
                fill = "blue")
        
        # 枠を描画
        canvas.create_rectangle(0, 0, SCREEN_WIDTH -1, SCREEN_HEIGHT -1, outline="grey", width=1)
            
        # 距離を描画
        canvas.create_text(5,5, text = "{:.2f}". format(dist), anchor = "nw", fill="red")
        canvas.update()
        
root.mainloop()    

