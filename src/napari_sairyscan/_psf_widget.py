from qtpy.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, QComboBox


class SPsfWidget(QGroupBox):
    """Widget to select a point spread function

    The point spread function can be selected from file or constructed from parameters

    """
    def __init__(self):
        super().__init__()
        self.setTitle('PSF')

        layout = QGridLayout()
        layout.addWidget(QLabel('model'), 0, 0)
        self.model_box = QComboBox()
        self.model_box.addItems('File', 'Gaussian')
        layout.addWidget(self.model_box, 1, 0)
        self.setLayout(layout)

    @staticmethod
    def check_inputs():
        return True

    def state(self):
        """Returns the psf widget parameters"""
        return {'model': self.model_box.currentText()}
