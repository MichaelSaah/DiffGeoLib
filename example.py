import DiffGeoLib as dgl
from math import cos, sin

astroid = lambda x: ((cos(x)**3), (sin(x)**3))
lemniscate = lambda x: (cos(x)/(1+sin(x)**2), (sin(x)*cos(x))/(1+sin(x)**2))
circle = lambda x: (cos(x),sin(x))

ani = dgl.animation.Animator(astroid, scale=100)

ani.run()