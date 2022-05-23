import os
from qtpy.QtWidgets import (QWidget, QGroupBox, QGridLayout, QLabel, QComboBox, QHBoxLayout,
                            QLineEdit, QPushButton, QFileDialog)
from skimage.io import imread
from sairyscan.enhancing._psfs import PSFGaussian


class SFileSelect(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.path_edit = QLineEdit()
        layout.addWidget(self.path_edit)
        browse_btn = QPushButton()
        browse_btn.released.connect(self._on_browse)
        layout.addWidget(browse_btn)
        self.setLayout(layout)

    def _on_browse(self):
        file = QFileDialog.getOpenFileName(self.widget, "Open a file", '', "*.*")
        if file != "":
            self.self.path_edit.setText(file[0])

    def check_inputs(self):
        return os.path.isfile(self.path_edit.text())

    def state(self):
        return self.path_edit.text()


class SGaussianWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel('Sigma'), 0, 0)
        self.sigma_edit = QLineEdit('1.5')
        layout.addWidget(self.sigma_edit, 0, 1)
        self.setLayout(layout)

    @staticmethod
    def check_inputs():
        return True

    def state(self):
        return self.sigma_edit.text()


class SPsfWidget(QWidget):
    """Widget to select a point spread function

    The point spread function can be selected from file or constructed from parameters

    """
    def __init__(self):
        super().__init__()
        # self.setTitle('PSF')

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel('psf'), 0, 0)
        self.model_box = QComboBox()
        self.model_box.addItems(['Gaussian', 'File'])
        self.model_box.currentTextChanged.connect(self._on_model_change)
        layout.addWidget(self.model_box, 0, 1)
        self.setLayout(layout)

        self.file_widget = SFileSelect()
        layout.addWidget(self.file_widget, 1, 0, 1, 2)

        self.gaussian_widget = SGaussianWidget()
        layout.addWidget(self.gaussian_widget, 2, 0, 1, 2)

        self._on_model_change('Gaussian')

    def _on_model_change(self, model):
        if model == 'File':
            self.file_widget.setVisible(True)
            self.gaussian_widget.setVisible(False)
        elif model == 'Gaussian':
            self.file_widget.setVisible(False)
            self.gaussian_widget.setVisible(True)

    @staticmethod
    def check_inputs():
        return True

    def state(self):
        """Returns the psf widget parameters"""
        if self.model_box.currentText() == 'File':
            data = imread(self.model_box.currentText())
        else:
            sigma = float(self.gaussian_widget.state())
            filter_ = PSFGaussian(sigma=(sigma, sigma), shape=(11, 11))
            data = filter_()
        return {'psf': data}
