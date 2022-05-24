import qtpy.QtCore
from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox

import torch

from sairyscan.core import SAiryscanPipeline
from sairyscan.reconstruction.spitfire_join_deconv import metadata as spitfire_metadata
from sairyscan.api import SAiryscanAPI

from ._splugin import SNapariWorker, SNapariWidget
from ._dict_widget import SDictWidget
from ._registration_widget import SRegistrationWidget


class SWidgetSpitfireJoinDeconv(SNapariWidget):
    def __init__(self):
        super().__init__()
        self.label = 'Spitfire Join Deconv'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.reg_widget = SRegistrationWidget()
        layout.addWidget(self.reg_widget)

        print('spitfire metadata:', spitfire_metadata)

        self.spitfire_widget = SDictWidget(spitfire_metadata)
        layout.addWidget(self.spitfire_widget)

        layout.addWidget(QWidget(), 1, qtpy.QtCore.Qt.AlignTop)

    def check_inputs(self):
        if self.reg_widget.check_inputs():
            return self.spitfire_widget.check_inputs()
        return False

    def state(self):
        state = self.reg_widget.state()
        return state.update(self.spitfire_widget.state())


class SWorkerSpitfireJoinDeconv(SNapariWorker):
    def __init__(self, napari_viewer, widget, observer):
        super().__init__(napari_viewer, widget)
        self.api = SAiryscanAPI()
        self._out_data = None
        self.image = None
        self._observer = observer

    def set_image(self, image):
        self.image = torch.Tensor(image)

    def run(self):
        reconstruction = self.api.filter('SpitfireJoinDeconv', **self.widget.spitfire_widget.state())
        registration = self.api.filter(self.widget.reg_widget.method(), **self.widget.reg_widget.state())
        pipeline = SAiryscanPipeline(reconstruction, registration=registration, enhancing=None)
        pipeline.add_observer(self._observer)
        self._out_data = pipeline(self.image).detach().numpy()
        self.finished.emit()

    def set_outputs(self):
        self.viewer.add_image(self._out_data, name='Spitfire Join Deconv')
