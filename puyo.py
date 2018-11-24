#!/usr/bin/env python
# -*- coding:utf-8 -*-

puyo_array = [
    "  GYRR",
    "RYYGYG",
    "GYGYRR",
    "RYGYRG",
    "YGYRYG",
    "GYRYRG",
    "YGYRYR",
    "YGYRYR",
    "YRRGRG",
    "RYGYGG",
    "GRYGYR",
    "GRYGYR",
    "GRYGYR",
]

# pythonの文字列はindex指定で書き換えられないのでbytearrayに変換
puyo = [ bytearray(line) for line in puyo_array ]

def show():
    print "-" * 8
    for x in puyo:
        print "|{}|".format(x)
    print "-" * 8
    print

def erase():
    u'''4つ以上繋がってるの消す'''
    class Way:
        u'''どっちから探索来たか'''
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    def mark(dx, dy, p, dst = None):
        u'''隣接してる同色を辿る'''
        if dx < 0 or dy < 0:
            return

        try:
            if puyo[dy][dx] == p:
                points.append((dx, dy))
                # 入ってきた方向に探索すると無限再帰するので
                if dst != Way.RIGHT:
                    mark(dx+1, dy, p, Way.LEFT)
                if dst != Way.UP:
                    mark(dx, dy+1, p, Way.DOWN)
                if dst != Way.LEFT:
                    mark(dx-1, dy, p, Way.RIGHT)
                if dst != Way.DOWN:
                    mark(dx, dy-1, p, Way.UP)
        except IndexError as e:
            pass

    for y, line in enumerate(puyo):
        for x, p in enumerate(line):
            if chr(p) != " ":
                points = []
                mark(x, y, puyo[y][x])

                if len(points) >= 4:    # 4連結以上
                    for x, y in points:
                        puyo[y][x] = " " # 消す

def drop():
    u'''浮いてるの落とす'''
    height = len(puyo)
    assert(height > 0)
    width = len(puyo[0])
    is_zenkeshi = True
    for x in range(width):
        for y in range(0, height)[::-1]:    # 下から嘗める
            if chr(puyo[y][x]) == " ":
                for y2 in range(0, y)[::-1]:
                    if chr(puyo[y2][x]) != " ":
                        puyo[y][x] = puyo[y2][x]
                        puyo[y2][x] = " "
                        break
            else:
                is_zenkeshi = False
    # 全部消えてたらTrue
    return is_zenkeshi


if __name__ == '__main__':
    import itertools
    for i in itertools.count():
        print i
        show()

        erase()
        if drop():
            break

    print "finish!!"
    show()
