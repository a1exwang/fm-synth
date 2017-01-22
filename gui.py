import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtCore import QObject
import numpy as np


class FMSynthGUI(QObject):
    update_graph_signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject',
                                     'PyQt_PyObject', 'PyQt_PyObject', name='graph_needs_updating')

    def __init__(self):
        super().__init__()
        self.app = QtGui.QApplication([])
        self.graphics_window = pg.GraphicsWindow(title="Spectrogram")
        self.graphics_window.resize(1200, 600)
        self.graphics_window.setWindowTitle('FM8 Synthesizer Main Panel')
        self.update_graph_signal.connect(self.update_graph)
        self.plot_count = 0

    @pyqtSlot('PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject', name='update_graph')
    def update_graph(self, curve, data, pl, resize):
        curve.setData(data)
        if resize:
            pl.enableAutoRange('x', False)

    @staticmethod
    def start():
        QtGui.QApplication.instance().exec_()

    def add_plot(self, title, *args, **kargs):
        if self.plot_count % 3 == 0:
            self.graphics_window.nextRow()
        self.plot_count += 1
        return self.graphics_window.addPlot(title=title, *args, **kargs)
