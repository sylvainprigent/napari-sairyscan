import qtpy.QtCore
from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox

import torch

from sairyscan.core import SAiryscanPipeline
from sairyscan.reconstruction.pseudo_confocal import metadata as confocal_metadata
from sairyscan.api import SAiryscanAPI

from ._splugin import SNapariWorker, SNapariWidget
from ._dict_widget import SDictWidget


class SWidgetConfocal(SNapariWidget):
    def __init__(self):
        super().__init__()
        self.label = 'Pseudo Confocal'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.confocal_widget = SDictWidget(confocal_metadata)
        layout.addWidget(self.confocal_widget)
        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignTop)

    def check_inputs(self):
        return self.confocal_widget.check_inputs()

    def state(self):
        return self.confocal_widget.state()


class SWorkerConfocal(SNapariWorker):
    def __init__(self, napari_viewer, widget, observer):
        super().__init__(napari_viewer, widget)
        self.api = SAiryscanAPI()
        self._out_data = None
        self.image = None
        self._observer = observer

    def set_image(self, image):
        self.image = torch.Tensor(image)

    def run(self):
        reconstruction = self.api.filter('PseudoConfocal', **self.widget.confocal_widget.state())
        pipeline = SAiryscanPipeline(reconstruction, registration=None, enhancing=None)
        pipeline.add_observer(self._observer)
        self._out_data = pipeline(self.image).detach().numpy()
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data, name='PseudoConfocal')
