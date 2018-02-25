import pygame as pg
import numpy as np
from collections import namedtuple, deque
from .curves import Curve

class Animator:
    """The Animator contains all of the logic for animating a curve.
    Simply pass it a function f: s -> (x,y) and call run().
    Click and drag to move around. Scroll to zoom."""

    def __init__(self, f, scale=1, size=(800, 600), ds=0.05, fps=30, max_hist=200):
        """Set up the animation environment.
        size: 2-tuple, Window size
        scale: Scalar, Default zoom
        ds: Size of time step
        fps: Framerate
        max_hist: The maximum number of previous points to keep"""

        self.Point = namedtuple('Point', ['x', 'y'])
        self.size = self.Point(*size)
        self.scale = scale
        self.origin = self.Point(self.size.x//2, self.size.y//2)
        self.curve = Curve(f)
        self.fps = fps
        if ds > 0:
            self.ds = ds
        else:
            raise ValueError('ds must be positive real number')
        self.s = 0

        pg.init()
        self.screen = pg.display.set_mode(self.size)
        self.slate = pg.Surface(self.size)
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()
        self.done = False
        self.drag = False
        self.history = deque(maxlen=max_hist)

        self.colors = {'k': (0, 0, 0),
                       'w': (255, 255, 255),
                       'b': (0, 0, 255),
                       'g': (0, 255, 0),
                       'r': (255, 0, 0)}

    def run(self):
        """Run the animation."""

        while not self.done:
            self.clock.tick(self.fps)
            last_mouse_pos = self.mouse_pos
            self.mouse_pos = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.dict['button'] == 4:  # scroll down
                        self.scale += self.scale * 0.08
                    elif event.dict['button'] == 5:  # scroll up
                        self.scale -= self.scale * 0.08
                    if event.dict['button'] == 1:  # L click
                        self.drag = True
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.dict['button'] == 1:  # L click
                        self.drag = False

            if self.drag:
                mouse_delta = tuple(np.subtract(self.mouse_pos, last_mouse_pos))
                self.origin = self.Point(*np.add(self.origin, mouse_delta))

            # clear surfaces
            self.screen.fill(self.colors['k'])
            self.slate.fill(self.colors['k'])

            # get new (unscaled) points from curve
            d0 = self.curve(self.s)
            self.history.append(d0)
            d1 = self.curve.derivative(self.s, self.ds/2, 1)
            d2 = self.curve.derivative(self.s, self.ds/2, 2)

            # draw curve points
            for pt in self.history:
                pt = self._translate_and_scale(pt)
                pt = list(map(lambda x: int(round(x)), pt))
                pg.draw.circle(self.slate, self.colors['w'], pt, 1)

            # draw derivative vectors
            d1 = np.add(d0,d1)
            d2 = np.add(d0,d2)
            d1 = self._translate_and_scale(d1)
            d2 = self._translate_and_scale(d2)
            d0 = self._translate_and_scale(d0)
            pg.draw.line(self.slate, self.colors['g'], d0, d2, 3)
            pg.draw.line(self.slate, self.colors['r'], d0, d1, 3)
            self.screen.blit(self.slate, (0, 0))

            pg.display.flip()

            self.s += self.ds

    def _translate_and_scale(self, point):
        """Scale point and translate for origin offset"""

        return self.origin.x + self.scale*point[0], self.origin.y - self.scale*point[1]