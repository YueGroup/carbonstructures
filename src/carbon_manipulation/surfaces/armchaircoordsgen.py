from math import sin, pi, cos

def rad(edges):
    n = edges
    r = 1.41 / (2 * sin(pi / (n * (2 + sin((pi / 2) - pi / (2 *n))))))
    return r