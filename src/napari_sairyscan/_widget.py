"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
import napari
from qtpy.QtWidgets import QGridLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QProgressBar
from qtpy.QtCore import QThread, Signal, QObject

from ._splugin import SProgressObserver
from ._ism import SWidgetISM, SWorkerISM
from ._ifed import SWidgetIFED, SWorkerIFED
from ._isfed import SWidgetISFED, SWorkerISFED
from ._pseudo_confocal import SWidgetConfocal, SWorkerConfocal


class SAiryscanWorker(QObject):
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._pipelines = {}
        self._current_method = ''

    def set_method(self, name):
        self._current_method = name

    def set_image(self, image):
        worker = self._pipelines[self._current_method]['worker']
        worker.set_image(image)

    def add_pipeline(self, label, pipeline_widget, pipeline_worker):
        self._pipelines.update({label: {'widget': pipeline_widget, 'worker': pipeline_worker}})

    def run(self):
        print('airyscan worker run start...')
        worker = self._pipelines[self._current_method]['worker']
        worker.run()
        print('airyscan worker run done (emit finished)')
        self.finished.emit()

    def current_worker(self):
        return self._pipelines[self._current_method]['worker']


class SAiryscanWidget(QWidget):
    finished = Signal()

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.viewer.events.layers_change.connect(self._on_layer_change)
        self.thread = QThread()
        self._worker = SAiryscanWorker()
        self._observer = SProgressObserver()
        self._widgets = {}

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
        self.parameters_layout.setContentsMargins(0, 0, 0, 0)
        parameters_widget.setLayout(self.parameters_layout)
        self.layout().addWidget(parameters_widget, 2, 0, 1, 2)

        # Run Button
        self.run_btn = QPushButton("Run")
        self.layout().addWidget(self.run_btn, 3, 0, 1, 2)
        self.run_btn.clicked.connect(self._on_click_run)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.layout().addWidget(self.progress_bar, 4, 0, 1, 2)
        self.layout().addWidget(QWidget(), 5, 0, 1, 2)

        # load the pipelines
        confocal_widget = SWidgetConfocal()
        confocal_worker = SWorkerConfocal(self.viewer, confocal_widget, self._observer)
        self.add_pipeline('Pseudo Confocal', confocal_widget, confocal_worker)

        ism_widget = SWidgetISM()
        ism_worker = SWorkerISM(self.viewer, ism_widget, self._observer)
        self.add_pipeline('ISM', ism_widget, ism_worker)

        ifed_widget = SWidgetIFED()
        ifed_worker = SWorkerIFED(self.viewer, ifed_widget, self._observer)
        self.add_pipeline('IFED', ifed_widget, ifed_worker)

        isfed_widget = SWidgetISFED()
        isfed_worker = SWorkerISFED(self.viewer, isfed_widget, self._observer)
        self.add_pipeline('ISFED', isfed_widget, isfed_worker)

        # init the view
        self._on_change_method(self.method_box.currentText())
        self._on_layer_change(None)

        # connect thread
        self._worker.moveToThread(self.thread)
        self.thread.started.connect(self._worker.run)
        self._worker.finished.connect(self.thread.quit)
        self._worker.finished.connect(self.set_outputs)
        self._observer.progress_signal.connect(self._on_progress)

    def add_pipeline(self, label, pipeline_widget, pipeline_worker):
        self._worker.add_pipeline(label, pipeline_widget, pipeline_worker)
        self._widgets.update({label: pipeline_widget})
        self.parameters_layout.addWidget(pipeline_widget)
        self.method_box.addItem(label)

    def set_outputs(self):
        worker = self._worker.current_worker()
        worker.set_outputs()

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
        print('self._widgets', self._widgets)
        widget = self._widgets[self.method_box.currentText()]
        self._worker.set_method(self.method_box.currentText())
        self._worker.set_image(self.viewer.layers[self.raw_data_layer_box.currentText()].data)
        if widget.check_inputs():
            self.thread.start()

    def _on_change_method(self, method_name):
        items = (self.parameters_layout.itemAt(i) for i in range(self.parameters_layout.count()))
        for w in items:
            if w.widget().label == method_name:
                w.widget().setVisible(True)
            else:
                w.widget().setVisible(False)

    def _on_progress(self, value):
        self.progress_bar.setValue(value)
