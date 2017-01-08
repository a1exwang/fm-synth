import pyqtgraph as pg
from PyQt5 import QtGui


class FMSynthGUI:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.graphics_window = pg.GraphicsWindow(title="Spectrogram")
        self.graphics_window.resize(1300, 500)
        self.graphics_window.setWindowTitle('FM8 Synthesizer Main Panel')

    @staticmethod
    def start():
        QtGui.QApplication.instance().exec_()

    def add_plot(self, title, *args, **kargs):
        return self.graphics_window.addPlot(title=title, *args, **kargs)
