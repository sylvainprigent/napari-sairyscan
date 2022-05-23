import qtpy.QtCore
from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox

import torch

from sairyscan.core import SAiryscanPipeline
from sairyscan.reconstruction.ifed import metadata as ifed_metadata
from sairyscan.api import SAiryscanAPI

from ._splugin import SNapariWorker, SNapariWidget
from ._dict_widget import SDictWidget


class SWidgetIFED(SNapariWidget):
    def __init__(self):
        super().__init__()
        self.label = 'IFED'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.ifed_widget = SDictWidget(ifed_metadata)
        layout.addWidget(self.ifed_widget)
        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignTop)

    def check_inputs(self):
        return self.ifed_widget.check_inputs()

    def state(self):
        return self.ifed_widget.state()


class SWorkerIFED(SNapariWorker):
    def __init__(self, napari_viewer, widget, observer):
        super().__init__(napari_viewer, widget)
        self.api = SAiryscanAPI()
        self._out_data = None
        self.image = None
        self._observer = observer

    def set_image(self, image):
        self.image = torch.Tensor(image)

    def run(self):
        print('run ifed with parameters:', self.widget.ifed_widget.state())
        reconstruction = self.api.filter('IFED', **self.widget.ifed_widget.state())
        pipeline = SAiryscanPipeline(reconstruction, registration=None, enhancing=None)
        pipeline.add_observer(self._observer)
        self._out_data = pipeline(self.image).detach().numpy()
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data, name='IFED')
