import macintoshplus
from PIL import Image
import numpy
from random import Random

random_seed = "blah"
win_path = Random(random_seed).choice(macintoshplus.windows)

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

bgcolor = "#008080"
im = Image.new("RGBA", (1000, 1000), bgcolor).convert("RGBA")
win = Image.open(win_path).convert("RGBA")

random_window = Random(random_seed).choice(macintoshplus.windows)
terrace = Image.open(random_window).convert("RGBA")

win = win.resize(map(lambda x: 3*x, win.size))
terrace = terrace.resize(map(lambda x: int(3*x), terrace.size))

def persp(src, top, t):
    mu = t/top*10 * 0.5 + 0.03
    width, height = src.size
    new_h = height - t
    coeffs = find_coeffs(

            [(0+t, 0), #top left
                (width - t /2, 0  + 30), #top right
                (width - t /2, height - 400), # bottom right
            (0+t, height)], #bottom left

            [(0, 0), (width, 0), (width, height), (0, height)])

    src = src.transform(src.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC,fill=0)
    return src

def make_tile(src, n):
    terrace_tile = Image.new("RGBA", src.size, bgcolor)
    tw,th = src.size
    src = src.resize((tw/n,th/n))
    for i in range(n):
        for j in range(n):
            terrace_tile.paste(src,(tw/n*i, th/n*j))
    return terrace_tile

tiled = make_tile(terrace,5)
tw, th = tiled.size
ratio = 0.42
offset = tiled.width * ratio
coeffs = find_coeffs(
        [(0+offset, 0+th/2), #top left
            (tw-offset, 0+th/2), #top right
            (tw, th), # bottom right
        (0, th)], #bottom left
        [(0, 0), (tw, 0), (tw, th), (0, th)])

tiled = tiled.transform(tiled.size, Image.PERSPECTIVE, coeffs, Image.BICUBIC,fill=0)


im.paste(tiled, 
    (
        int(im.width-tiled.width * (1-0.9*ratio)),
        im.height-tiled.height + 80
    ),
    tiled)

for density in range(40, 45, 5):
    top =  600
    increment = density
    stack = []
    for i in range(0,top, increment):
        out = persp(win, top, i)
        if (i < top // 2 + increment ):
            im.paste(out, (i,20), out)
        else:
            stack.append((i,out))
    stack.reverse()
    for (i, out) in stack:
        im.paste(out,(i,20),out)
    random_bubble = Random(random_seed).choice(macintoshplus.bubbles)
    im = macintoshplus.insert_bubble(random_bubble, im)
    fname = 'output/mac'+ str(density) +'.png'

    print fname
    im.save(fname)
    im.save('mac.png')

