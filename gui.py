from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class FMSynthGUI:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Spectrogram")
        self.win.resize(1300, 500)
        self.win.setWindowTitle('FM8 Synthesizer Main Panel')
        # pg.setConfigOptions(antialias=True)

    @staticmethod
    def start():
        QtGui.QApplication.instance().exec_()

    def add_plot(self, title, *args, **kargs):
        return self.win.addPlot(title=title, *args, **kargs)
