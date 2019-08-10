import pyqtgraph as pg
import math


class LogValueAxis(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            # vs is the original tick value
            vs = v * scale
            vstr = '%0.0f' % (math.exp(vs),)
            strings.append(vstr)
        return strings

