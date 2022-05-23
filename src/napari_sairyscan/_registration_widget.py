from qtpy.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QComboBox, QGroupBox
from ._dict_widget import SDictWidget
from sairyscan.registration import SRegisterPosition, SRegisterMSE, metadata


class SRegistrationWidget(QGroupBox):
    """Widget to select and setup a registration method"""
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
            self.registration_box.addItem(meta['label'], meta['name'])
            widget = SDictWidget(meta)
            self.parameters_layout.addWidget(widget)

        self.registration_box.currentTextChanged.connect(self._on_box_change)
        self._on_box_change(self.registration_box.currentText())

    def method(self):
        """Returns the current registration method label"""
        print('registration widget current data=', self.registration_box.currentData())
        return self.registration_box.currentData()

    @staticmethod
    def check_inputs():
        return True

    def state(self):
        """Returns the current registration method parameters (dict)"""
        text = self.registration_box.currentText()
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            if w.widget().metadata['label'] == text:
                return w.widget().state()
        return {}

    def _on_box_change(self, text):
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            if w.widget().metadata['label'] == text:
                w.widget().setVisible(True)
            else:
                w.widget().setVisible(False)
