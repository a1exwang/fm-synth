from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from channels.channel import Channel


class DoubleSlider(QSlider):
    # create our our signal that we can connect to if necessary
    doubleValueChanged = pyqtSignal(float)

    def __init__(self, *args, **kwargs):
        super(DoubleSlider, self).__init__(*args, **kwargs)
        self._min_value = 0
        self._max_value = 1
        self._step = 0.01
        self.valueChanged.connect(self.emitDoubleValueChanged)

    def _step_count(self):
        return int((self._max_value - self._min_value) / self._step)

    def emitDoubleValueChanged(self):
        value = (float(super(DoubleSlider, self).value()) + self._min_value) * self._step
        self.doubleValueChanged.emit(value)

    def setRange(self, range_min, range_max):
        assert range_min < range_max
        self._min_value = range_min
        self._max_value = range_max
        super(DoubleSlider, self).setRange(0, self._step_count())

    def singleStep(self):
        return self._step

    def setSingleStep(self, value):
        self._step = value
        assert value > 0
        assert self._step_count() > 0
        super(DoubleSlider, self).setRange(0, self._step_count())
        return super(DoubleSlider, self).setSingleStep(1)

    def value(self):
        int_value = super(DoubleSlider, self).value()
        return (float(int_value) + self._min_value) * self._step

    def setValue(self, value):
        super(DoubleSlider, self).setValue(int((value - self._min_value) / self._step))


class ConnectSlider(QWidget):
    def __init__(self, name):
        super().__init__(flags=Qt.Widget)
        self.name = name
        self.channel = Channel.get_instance()
        self.connected_channel = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.slider = DoubleSlider()
        self.channel_selector = QComboBox()
        self.label_value = QLabel(text='0')
        self.label_name = QLabel(text=self.name)

        self.channel_selector.setEditable(True)
        self.channel_selector.addItems(['Unconnected'] + self.channel.get_channels())
        self.channel_selector.currentIndexChanged.connect(self.channel_selected)
        self.channel_selector.setInsertPolicy(QComboBox.NoInsert)
        self.connected_channel = None

        self.slider.doubleValueChanged.connect(self.slider_changed)

        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.channel_selector)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label_value)
        self.layout.setAlignment(Qt.AlignRight)

    @pyqtSlot(float, name='slider_changed')
    def slider_changed(self, val):
        self.label_value.setText(str(val))
        if self.connected_channel:
            self.connected_channel(val)

    @pyqtSlot(int, name='channel_selected')
    def channel_selected(self, index):
        if index > 0:
            name = self.channel.get_channels()[index - 1]

            # NOTE(aocheng):
            #  The slot must set before the range and step is set, or the old channel will have a wrong value.
            slot = self.channel.get_channel(name)
            self.connected_channel = slot

            get_val = self.channel.get_channel_val(name)

            range_min, range_max, step = self.channel.get_channel_range_and_step(name)()
            self.slider.setRange(range_min, range_max)
            self.slider.setSingleStep(step)
            self.slider.setValue(get_val())
