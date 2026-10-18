import random
import math
import time
import os

WIDTH = 80
HEIGHT = 30

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# ---------- 1. 生成不重叠的星星 ----------
# 把所有坐标列出来，打乱后取前 N 个，保证不重复
all_positions = [(x, y) for y in range(HEIGHT) for x in range(WIDTH)]
random.shuffle(all_positions)

stars = []
for (x, y) in all_positions[:150]:      # 取 150 个，保证不重叠
    stars.append({
        "x": x,
        "y": y,
        "speed": random.uniform(0.05, 0.3),
        "phase": random.uniform(0, 6.28),
    })

# ---------- 2. 爱心公式 ----------
def is_in_heart(x, y):
    # 把画布坐标转成数学坐标，爱心居中
    xf = (x - WIDTH / 2) / 9
    yf = -(y - HEIGHT / 2) / 9    # 注意 y 要翻转，因为终端 y 向下
    return (xf**2 + yf**2 - 1)**3 - xf**2 * yf**3 <= 0

# ---------- 3. 每帧渲染 ----------
def render(frame):
    # 建空画布
    canvas = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # 先画星星（会被爱心覆盖）
    for s in stars:
        brightness = math.sin(frame * s["speed"] + s["phase"])
        char = "✦" if brightness > 0.3 else ("·" if brightness > -0.5 else " ")
        canvas[s["y"]][s["x"]] = char

    # 再画爱心（覆盖星星），爱心自身也随 sin 缩放
    scale = 9 + math.sin(frame * 0.15) * 1.5
    for y in range(HEIGHT):
        for x in range(WIDTH):
            xf = (x - WIDTH / 2) / scale
            yf = -(y - HEIGHT / 2) / scale
            if (xf**2 + yf**2 - 1)**3 - xf**2 * yf**3 <= 0:
                canvas[y][x] = "*"

    # 输出
    clear()
    for row in canvas:
        print("".join(row))

# ---------- 4. 主循环 ----------
frame = 0
while True:
    render(frame)
    frame += 1
    time.sleep(0.06)