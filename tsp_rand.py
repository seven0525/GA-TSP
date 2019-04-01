# coding: utf8
import sys
import random
import math
import copy
import tkinter

# パラメーター
SCREEN_WIDTH  = 360
SCREEN_HEIGHT = 360
POINTS_SIZE = 50 # 都市の数
LOOP = 100000 # 探索回数

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

# メイン処理
# ウィンドウ初期化
root = tkinter.Tk()
root.title("TSPを乱数だけで解いてみる")
root.geometry(str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT))

# キャンバスを生成
canvas = tkinter.Canvas(root, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
canvas.place(x=0, y=0)

# 都市の座標を生成
points = []
for i in range(POINTS_SIZE):
    points.append((random.random(), random.random()))

# 各都市を一巡する経路を作成
route = list(range(POINTS_SIZE))

min_route = copy.copy(route)
min_dist = calc_distance(points, route)

for c in range(LOOP):
    root.title(u"TSPを乱数だけで解いてみる（" + str(c +  1) + u"回）")
    
    # 巡回する順番をランダムで入れ替える
    random.shuffle(route)

    dist = calc_distance(points, route)

    # より短い経路が見つかった場合
    if min_dist > dist:
        min_route = copy.copy(route)
        min_dist = dist

        canvas.delete("all")
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
                x0 * SCREEN_WIDTH - 3,
                y0 * SCREEN_HEIGHT - 3,
                x0 * SCREEN_WIDTH + 3,
                y0 * SCREEN_HEIGHT + 3,
                fill = "blue")
            
        # 距離を描画
        canvas.create_text(5,5, text = "{:.2f}". format(min_dist), anchor = "nw", fill="red")
        canvas.update()
    
root.mainloop()

