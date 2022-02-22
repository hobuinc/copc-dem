
import sys
from . import logs

class Bounds(object):
    def __init__(self, minx, miny, maxx, maxy, resolution, srs=None):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.resolution = resolution
        self.srs = srs
        self.rangex = self.maxx - self.minx
        self.rangey = self.maxy - self.miny

    def split(self):
        centerx = self.minx + self.rangex/2.0
        centery = self.miny + self.rangey/2.0

        ll = Bounds(self.minx, self.miny, centerx, centery, self.resolution, self.srs)
        ul = Bounds(self.minx, centery, centerx, self.maxy, self.resolution, self.srs)
        ur = Bounds(centerx, centery, self.maxx, self.maxy, self.resolution, self.srs)
        lr = Bounds(centerx, self.miny, self.maxx, centery, self.resolution, self.srs)
        bounds = [ll, ul, ur, lr]

        output = yield from bounds

    def buffer(self, buffer = None, negative=False):

        if negative:
            if abs(self.rangex-buffer) <= abs(buffer) or \
                abs(self.rangey - buffer) <= abs(buffer):
                    logger.debug("failed to negative buffer")
                    return self
            minx = self.minx + buffer
            miny = self.miny + buffer
            maxx = self.maxx - buffer
            maxy = self.maxy - buffer
        else:
            minx = self.minx - buffer
            miny = self.miny - buffer
            maxx = self.maxx + buffer
            maxy = self.maxy + buffer
        return Bounds(minx, miny, maxx, maxy, self.resolution, self.srs)

    def __repr__(self):
        return self.__str__() + f' rangex: {self.rangex} -- rangey: {self.rangey} res: {self.resolution}'

    def __str__(self):
        return f"([{self.minx:.2f},{self.maxx:.2f}],[{self.miny:.2f},{self.maxy:.2f}])"


MaxBounds = Bounds(sys.float_info.max, sys.float_info.max, sys.float_info.min, sys.float_info.min, 200000, None)