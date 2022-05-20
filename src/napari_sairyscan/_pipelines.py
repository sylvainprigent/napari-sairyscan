from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox
from sairyscan.reconstruction import IFED, ISFED, ISM, PseudoConfocal, SpitfireReconstruction
from sairyscan.registration import SRegisterPosition, SRegisterMSE, metadata
from ._gui import SDictWidget


class SRegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        registration_box = QComboBox()

        layout.addWidget(QLabel('Registration'), 0, 0)
        layout.addWidget(registration_box, 0, 1)

        self.parameters_widgets = QWidget()
        self.parameters_layout = QVBoxLayout()
        self.parameters_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.parameters_widgets, 1, 0, 1, 2)

        # add all the items
        for meta in metadata:
            registration_box.addItem(meta['label'])
            widget = SDictWidget(meta)
            self.parameters_layout.addWidget(widget)

        registration_box.currentTextChanged.connect(self._on_box_change)

    def _on_box_change(self, text):
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            print('registration widget metadata:', w.widget().metadata)
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
        self.label = 'ISM'

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.reg_widget = SRegistrationWidget()
        layout.addWidget(self.reg_widget)

    def run(self):
        pass
