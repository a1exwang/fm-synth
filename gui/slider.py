from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from channels.channel import Channel
import pdb


class ConnectSlider(QWidget):
    def __init__(self, name):
        super().__init__(flags=Qt.Widget)
        self.name = name
        self.channel = Channel.get_instance()
        self.connected_channel = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.slider = QSlider()
        self.channel_selector = QComboBox()
        self.label_value = QLabel(text='0')
        self.label_name = QLabel(text=self.name)

        self.channel_selector.setEditable(True)
        self.channel_selector.addItems(['Unconnected'] + self.channel.get_channels())
        self.channel_selector.currentIndexChanged.connect(self.channel_selected)
        self.channel_selector.setInsertPolicy(QComboBox.NoInsert)
        self.connected_channel = None

        self.slider.valueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.channel_selector)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label_value)
        self.layout.setAlignment(Qt.AlignRight)

    @pyqtSlot(int, name='slider_changed')
    def slider_changed(self, val):
        self.label_value.setText(str(val))
        if self.connected_channel:
            self.connected_channel(val / self.slider.maximum())

    @pyqtSlot(int, name='channel_selected')
    def channel_selected(self, index):
        if index > 0:
            name = self.channel.get_channels()[index - 1]
            slot = self.channel.get_channel(name)
            get_val = self.channel.get_channel_val(name)
            get_max_val = self.channel.get_channel_max(name)
            self.slider.setMaximum(get_max_val())
            self.connected_channel = slot
            self.slider.setValue(int(get_val() * self.slider.maximum()))
