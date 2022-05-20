"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
import napari
from qtpy.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QProgressBar

from ._pipelines import SPipelineISM


class SAiryscanWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.viewer.events.layers_change.connect(self._on_layer_change)

        self.setLayout(QGridLayout())

        # Raw data layer
        self.layout().addWidget(QLabel('Raw data'), 0, 0)
        self.raw_data_layer_box = QComboBox()
        self.layout().addWidget(self.raw_data_layer_box, 0, 1)

        # Method
        self.layout().addWidget(QLabel('Method'), 1, 0)
        self.method_box = QComboBox()
        self.layout().addWidget(self.method_box, 1, 1)
        self.method_box.currentTextChanged.connect(self._on_change_method)

        # Method parameters
        parameters_widget = QWidget()
        self.parameters_layout = QVBoxLayout()
        parameters_widget.setLayout(self.parameters_layout)
        self.layout().addWidget(parameters_widget, 2, 0, 1, 2)

        # Run Button
        self.run_btn = QPushButton("Run")
        self.layout().addWidget(self.run_btn, 3, 0, 1, 2)
        self.run_btn.clicked.connect(self._on_click_run)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(42)
        self.layout().addWidget(self.progress_bar, 4, 0, 1, 2)
        self.layout().addWidget(QWidget(), 5, 0, 1, 2)

        # load the pipelines
        self.add_pipeline(SPipelineISM())

    def add_pipeline(self, pipeline_widget):
        self.parameters_layout.addWidget(pipeline_widget)
        self.method_box.addItem(pipeline_widget.label)

    def _on_layer_change(self, e):
        """Update the plugin layers lists when napari layers are updated

        Parameters
        ----------
        e: QObject
            Qt event

        """
        self.raw_data_layer_box.clear()
        for layer in self.viewer.layers:
            if isinstance(layer, napari.layers.image.image.Image):
                self.raw_data_layer_box.addItem(layer.name)
        if self.raw_data_layer_box.count() < 1:
            self.run_btn.setEnabled(False)
        else:
            self.run_btn.setEnabled(True)

    def _on_click_run(self):
        print("napari has", len(self.viewer.layers), "layers")

    def _on_change_method(self, method_name):
        print("Current method is ", method_name, " for layer:", len(self.viewer.layers))
