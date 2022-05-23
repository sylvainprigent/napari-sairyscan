from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox
from sairyscan.core import SAiryscanPipeline
from sairyscan.reconstruction.ism import metadata as ism_metadata
from sairyscan.reconstruction.ifed import metadata as ifed_metadata
from sairyscan.api import SAiryscanAPI
from ._dict_widget import SDictWidget


class SRegistrationWidget(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setTitle('Registration')

        layout = QGridLayout()
        layout.setContentsMargins(3, 11, 3, 11)
        self.setLayout(layout)

        self.registration_box = QComboBox()

        layout.addWidget(QLabel('Method'), 0, 0)
        layout.addWidget(self.registration_box, 0, 1)

        self.parameters_widgets = QWidget()
        self.parameters_layout = QVBoxLayout()
        self.parameters_layout.setContentsMargins(0, 0, 0, 0)
        self.parameters_widgets.setLayout(self.parameters_layout)
        layout.addWidget(self.parameters_widgets, 1, 0, 1, 2)

        # add all the items
        for meta in metadata:
            self.registration_box.addItem(meta['label'])
            widget = SDictWidget(meta)
            self.parameters_layout.addWidget(widget)

        self.registration_box.currentTextChanged.connect(self._on_box_change)
        self._on_box_change(self.registration_box.currentText())

    def method(self):
        """Returns the current registration method label"""
        return self.registration_box.currentText()

    def parameters(self):
        """Returns the current registration method parameters (dict)"""
        text = self.registration_box.currentText()
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            if w.widget().metadata['label'] == text:
                return w.widget.parameters()
        return {}

    def _on_box_change(self, text):
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            if w.widget().metadata['label'] == text:
                w.widget().setVisible(True)
            else:
                w.widget().setVisible(False)


class SPipelineGui(QWidget):
    def __init__(self):
        super().__init__()

    def run(self):
        raise NotImplementedError('Default pipeline is not implemented')


class SPipelineISM(SPipelineGui):
    def __init__(self):
        super().__init__()
        self.api = SAiryscanAPI()
        self.label = 'ISM'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.reg_widget = SRegistrationWidget()
        layout.addWidget(self.reg_widget)

        self.ism_widget = SDictWidget(ism_metadata)
        layout.addWidget(self.ism_widget)

    def run(self):
        reconstruction = self.api.filter('ISM', {})
        registration = self.api.filter(self.reg_widget.method(), **self.reg_widget.parameters())
        pipeline = SAiryscanPipeline(reconstruction, registration=registration, enhancing=None)
        return pipeline()


class SPipelineIFED(SPipelineGui):
    def __init__(self):
        super().__init__()
        self.api = SAiryscanAPI()
        self.label = 'IFED'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.ifed_widget = SDictWidget(ifed_metadata)
        layout.addWidget(self.ifed_widget)

    def run(self):
        reconstruction = self.api.filter('IFED', self.ifed_widget.parameters())
        pipeline = SAiryscanPipeline(reconstruction, registration=None, enhancing=None)
        return pipeline()
