import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QHBoxLayout
from pprint import pprint
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtCore import QUrl
import os
from api.main import start_web_server, set_data

import PyQt5.Qt
from gui.slider import ConnectSlider
from channels.channel import Channel


class FMSynthGUI(QObject):
    update_graph_signal = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject',
                                     'PyQt_PyObject', 'PyQt_PyObject', name='graph_needs_updating')

    def __init__(self):
        super().__init__()
        self.app = QtGui.QApplication([])

        self.graphics_window = pg.GraphicsWindow()
        self.graphics_window.resize(800, 450)
        self.graphics_window.setWindowTitle('FM8 Synthesizer Main Panel')
        self.update_graph_signal.connect(self.update_graph)
        self.plot_count = 0

        self.slider_panel = QWidget(flags=Qt.Widget)
        self.slider_panel.resize(300, 200)
        self.sp_layout = QHBoxLayout()
        self.slider_panel.setLayout(self.sp_layout)
        self.sliders = []
        self.slider_panel.show()
        self.web_view = QWebView()

    def post_init(self, out):
        for i in range(5):
            s = ConnectSlider(name='Slider %g' % i)
            self.sliders.append(s)
            self.sp_layout.addWidget(s)

        ops = []
        out.dump(ops)
        pprint(ops)

        start_web_server()
        objs = []
        out.dump(objs)
        set_data(objs)

        path = os.path.abspath(os.path.dirname(__file__)) + '/../web/main.html'
        self.web_view.load(QUrl.fromLocalFile(path))
        # self.web_view.page().settings().setAttribute(QWebEngineSettings)
        self.web_view.show()

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
