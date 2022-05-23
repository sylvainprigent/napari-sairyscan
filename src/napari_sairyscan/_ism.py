import qtpy.QtCore
from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox

import torch

from sairyscan.core import SAiryscanPipeline
from sairyscan.reconstruction.ism import metadata as ism_metadata
from sairyscan.api import SAiryscanAPI

from ._splugin import SNapariWorker, SNapariWidget
from ._dict_widget import SDictWidget
from ._registration_widget import SRegistrationWidget
from ._enhancing_widget import SEnhancingWidget


class SWidgetISM(SNapariWidget):
    def __init__(self):
        super().__init__()
        self.label = 'ISM'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.reg_widget = SRegistrationWidget()
        layout.addWidget(self.reg_widget)

        self.ism_widget = SDictWidget(ism_metadata)
        layout.addWidget(self.ism_widget)

        self.enhancing_widget = SEnhancingWidget()
        layout.addWidget(self.enhancing_widget)

        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignTop)

    def check_inputs(self):
        if self.reg_widget.check_inputs():
            if self.ism_widget.check_inputs():
                return self.enhancing_widget.check_inputs()
        return False

    def state(self):
        state = self.reg_widget.state()
        state = state.update(self.ism_widget.state())
        return state.update(self.enhancing_widget.state())


class SWorkerISM(SNapariWorker):
    def __init__(self, napari_viewer, widget, observer):
        super().__init__(napari_viewer, widget)
        self.api = SAiryscanAPI()
        self._out_data = None
        self.image = None
        self._observer = observer

    def set_image(self, image):
        self.image = torch.Tensor(image)

    def run(self):
        reconstruction = self.api.filter('ISM', **{})
        registration = self.api.filter(self.widget.reg_widget.method(), **self.widget.reg_widget.state())
        enhancing = self.api.filter(self.widget.enhancing_widget.method(), **self.widget.enhancing_widget.state())
        pipeline = SAiryscanPipeline(reconstruction, registration=registration, enhancing=enhancing)
        pipeline.add_observer(self._observer)
        self._out_data = pipeline(self.image).detach().numpy()
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data, name='ISM')
